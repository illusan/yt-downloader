import customtkinter as ctk
import threading
import os
import shutil
from tkinter import messagebox, PhotoImage
import yt_dlp

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("yt mp3/mp4 downloader")
app.geometry("800x600")

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
app_icon = PhotoImage(file=icon_path)
app.iconphoto(True, app_icon)

def update_ui(percent):
    progress_bar.set(percent)
    progress_label.configure(text=f"{int(percent * 100)}%")

def set_status(text):
    status_label.configure(text=text)

def show_progress():
    status_label.pack(pady=(20, 5))
    progress_bar.pack(pady=(0, 5))
    progress_label.pack()

def hide_progress():
    status_label.pack_forget()
    progress_bar.pack_forget()
    progress_label.pack_forget()

def reset_ui():
    button.configure(state="normal", text="Download")
    hide_progress()
    update_ui(0.0)

def progress_hook(d):
    if d['status'] == 'downloading':
        info = d.get('info_dict', {})
        if info.get('vcodec') not in (None, 'none'):
            app.after(0, set_status, "Downloading video...")
        else:
            app.after(0, set_status, "Downloading audio...")

        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        if total > 0:
            downloaded = d.get('downloaded_bytes', 0)
            app.after(0, update_ui, downloaded / total)
    elif d['status'] == 'finished':
        app.after(0, update_ui, 1.0)

def postprocessor_hook(d):
    if d['status'] == 'started':
        if d['postprocessor'] == 'ExtractAudio':
            app.after(0, set_status, "Converting to MP3...")
        elif d['postprocessor'] == 'Merger':
            app.after(0, set_status, "Merging video and audio...")

def on_success(fmt):
    messagebox.showinfo("Done!", f"Download completed! The {fmt} file has been saved in your Downloads folder.")
    entry.delete(0, 'end')

def on_error(message):
    messagebox.showerror("Download error", f"An error occurred:\n{message}")

def download_video(url, fmt):
    try:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        output_template = os.path.join(downloads_path, '%(title)s.%(ext)s')

        ydl_opts = {
            'outtmpl': output_template,
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'postprocessor_hooks': [postprocessor_hook],
        }

        if fmt == "MP3":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            ydl_opts['merge_output_format'] = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        app.after(0, on_success, fmt)

    except Exception as e:
        app.after(0, on_error, str(e))

    finally:
        app.after(0, reset_ui)

def start_download_thread():
    url = entry.get().strip()
    fmt = option.get()

    if not url:
        messagebox.showwarning("Missing URL", "Enter a video URL first!")
        return

    if shutil.which("ffmpeg") is None:
        messagebox.showerror("ffmpeg not found", "ffmpeg is required for MP3 and MP4 downloads.\nInstall it with: brew install ffmpeg")
        return

    if shutil.which("deno") is None:
        messagebox.showerror("deno not found", "deno is required, otherwise YouTube blocks downloads (HTTP 403).\nInstall it with: brew install deno")
        return

    button.configure(state="disabled", text="Downloading..")
    set_status("Starting...")
    update_ui(0.0)
    show_progress()

    thread = threading.Thread(target=download_video, args=(url, fmt), daemon=True)
    thread.start()


text = ctk.CTkLabel(app, text="YouTube to mp3 / mp4 converter", font=("Arial", 40), bg_color="transparent")
text.pack(pady=(30, 0))
text2 = ctk.CTkLabel(app, text="free mp3 and mp4 format converter, compatible with YouTube", font=("Arial", 17), bg_color="transparent")
text2.pack(pady=(5, 0))


frame = ctk.CTkFrame(app, bg_color="transparent")
frame.pack(pady=10)

entry = ctk.CTkEntry(frame, width=500, placeholder_text="enter video URL")
entry.grid(row=0, column=0, padx=10, pady=10)

option = ctk.CTkOptionMenu(frame, values=["MP3", "MP4"], width=70)
option.grid(row=0, column=1, padx=10, pady=10)
option.set("MP3")

button = ctk.CTkButton(frame, text="Download", command=start_download_thread)
button.grid(row=1, column=0, columnspan=2, pady=20)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 15))

progress_bar = ctk.CTkProgressBar(app, width=500)
progress_bar.set(0)

progress_label = ctk.CTkLabel(app, text="0%", font=("Arial", 15))

app.mainloop()
