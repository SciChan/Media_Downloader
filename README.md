# Media Downloader — Streamlit App

A clean, beautifully structured, light-themed media downloader built with Python, Streamlit, and yt-dlp.

## Features
- Paste links from supported social platforms (Instagram, TikTok, Twitter/X, Facebook, Reddit, Vimeo, Spotify, SoundCloud, Twitch, Dailymotion)
- Fetches and displays video info (title, channel, duration, views, thumbnail)
- Choose from available formats: multiple resolutions up to 4K (Video + Audio) or MP3 audio-only
- Live progress bar during download
- One-click save to your device
- **YouTube downloading is intentionally disabled** to guarantee cloud server stability and prevent IP bans.

## Local Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg (Required for High Quality):**
   - **macOS:** `brew install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt install ffmpeg`
   - **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add the `bin` folder to your system PATH.

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   The app opens at **http://localhost:8501** in your browser.

## Deployment (Streamlit Community Cloud)

This app is ready to easily deploy on Streamlit Community Cloud:

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and create a "New app".
3. Select your repository and point to `app.py`.
4. Streamlit Cloud will automatically install Python libraries from `requirements.txt` and install `ffmpeg` system-wide using `packages.txt`.

## Disclaimer
> ⚠️ Only download content you have the right to use. This tool is intended for personal, offline viewing of media you own or have permission to download.
