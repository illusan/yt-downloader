<p align="center">
  <img src="icon.png" width="128" alt="App icon">
</p>

<h1 align="center">yt mp3/mp4 downloader</h1>

<p align="center">A simple desktop app for downloading YouTube videos as MP3 or MP4.</p>

---

## Features

- Download as **MP3** (192 kbps audio) or **MP4** (best quality video + audio)
- Progress bar with live status: downloading video / audio, converting, merging
- Files are saved straight to your `Downloads` folder
- Dark mode UI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/): converts to MP3 and merges video with audio
- [deno](https://deno.com/): yt-dlp needs it to download from YouTube (without it you get `HTTP Error 403: Forbidden`)

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/illusan/yt-mp3-mp4-downloader-app.git
   cd yt-mp3-mp4-downloader-app
   ```
2. Install ffmpeg and deno (macOS, with [Homebrew](https://brew.sh/)):
   ```bash
   brew install ffmpeg deno
   ```
3. Install the Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

```bash
python3 main.py
```

1. Paste a YouTube video URL
2. Pick **MP3** or **MP4**
3. Click **Download**

The file lands in `~/Downloads`.

## Troubleshooting

| Error | Fix |
| --- | --- |
| `HTTP Error 403: Forbidden` | Install deno (`brew install deno`) and update yt-dlp: `pip3 install -U "yt-dlp[default]"` |
| `CERTIFICATE_VERIFY_FAILED` | Run `pip3 install certifi`, or on macOS run `Install Certificates.command` from your Python folder in `/Applications` |
| `ffmpeg not found` | `brew install ffmpeg` |

## Disclaimer

For personal use only. Download only content you have the rights to, and follow YouTube's Terms of Service.
