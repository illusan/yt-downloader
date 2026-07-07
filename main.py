import customtkinter as ctk
import threading
import os
from tkinter import messagebox
import yt_dlp
from tkinter import ttk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("yt mp3/mp4 downloader")
app.geometry("800x600")

def download_video():
    url = entry.get()
    fmt = option.get()

    if not url:
        messagebox.showwarning("Error", "Enter a video URL first!")
        button.configure(state="normal", text="Download")
        return
    
    button.configure(state="disabled", text="Downloading..")


# ----- Part done by AI

    try:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        output_template = os.path.join(downloads_path, '%(title)s.%(ext)s')

        if fmt == "MP3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'nocheckcertificate': True,
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': output_template,
                'nocheckcertificate': True,
                'noplaylist': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        messagebox.showinfo("Done!", f"Download completed! The {fmt} file has been saved in your Downloads folder.")
        entry.delete(0, 'end')
        
    except Exception as e:
        messagebox.showerror("Download error", f"An error occurred:\n{str(e)}")
        
    finally:
        button.configure(state="normal", text="Download")

# -----

    
def start_download_thread():
    thread = threading.Thread(target=download_video)
    thread.start()


text = ctk.CTkLabel(app, text="YouTube to mp3 / mp4 conventer", font=("Arial", 40), bg_color="transparent")
text.pack(pady=(30, 0))
text2 = ctk.CTkLabel(app, text="free mp3 and mp4 format converter, compatibile with YouTube", font=("Arial", 17), bg_color="transparent")
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



app.mainloop()