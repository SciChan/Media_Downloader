import streamlit as st
import yt_dlp
import os
import tempfile
import re
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Media Downloader",
    page_icon="▶",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;1,9..40,300&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #f8f9fa !important;
}
[data-testid="stAppViewContainer"] > .main {
    background: #f8f9fa;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stDecoration"] { display: none; }
section.main > div { padding-top: 4rem; padding-bottom: 4rem; }

/* ── Typography ── */
* { font-family: 'DM Sans', sans-serif; color: #212529; }

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 0.08em;
}

/* ── Hero title ── */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 10vw, 6rem);
    line-height: 0.9;
    letter-spacing: 0.05em;
    color: #111111;
    margin: 0;
    margin-bottom: 0.5rem;
}
.hero-accent {
    color: #ff3c00;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 400;
    color: #6c757d;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 1rem;
    margin-bottom: 2rem;
}

/* ── Divider ── */
.red-line {
    height: 3px;
    background: linear-gradient(90deg, #ff3c00, transparent);
    border: none;
    margin: 2rem 0 3rem 0;
}

/* ── Input fields ── */
[data-testid="stTextInput"] input {
    background: #ffffff !important;
    border: 1px solid #ced4da !important;
    border-radius: 8px !important;
    color: #212529 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #ff3c00 !important;
    box-shadow: 0 0 0 3px rgba(255,60,0,0.15) !important;
}
[data-testid="stTextInput"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #495057 !important;
    margin-bottom: 0.5rem !important;
}

/* ── Select boxes ── */
[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid #ced4da !important;
    border-radius: 8px !important;
    color: #212529 !important;
    padding: 0.2rem !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}
[data-testid="stSelectbox"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #495057 !important;
    margin-bottom: 0.5rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #ff3c00 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.8rem 2rem !important;
    transition: background 0.2s, transform 0.1s, box-shadow 0.2s !important;
    width: 100%;
    box-shadow: 0 4px 6px rgba(255,60,0,0.2) !important;
    margin-top: 1rem;
}
.stButton > button:hover {
    background: #e03400 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(255,60,0,0.25) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #ff3c00 !important;
    border: 2px solid #ff3c00 !important;
    border-radius: 6px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.8rem 2rem !important;
    transition: all 0.2s !important;
    width: 100%;
    margin-top: 1rem;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #ff3c00 !important;
    color: #fff !important;
    box-shadow: 0 4px 6px rgba(255,60,0,0.2) !important;
}

/* ── Info card ── */
.info-card {
    background: #ffffff;
    border: 1px solid #e9ecef;
    border-left: 4px solid #ff3c00;
    border-radius: 8px;
    padding: 2.5rem 2rem;
    margin: 2.5rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}
.info-card .title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.04em;
    color: #212529;
    margin-bottom: 0.5rem;
}
.info-card .meta {
    font-size: 0.9rem;
    color: #6c757d;
    letter-spacing: 0.05em;
}
.info-card .meta span {
    color: #495057;
    font-weight: 600;
}

/* ── Status messages ── */
.stAlert {
    background: #ffffff !important;
    border: 1px solid #e9ecef !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}
[data-testid="stNotification"] {
    background: #ffffff !important;
    border: 1px solid #e9ecef !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: #ff3c00 !important;
}

/* ── Thumbnail ── */
.thumb-wrap {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

/* ── Radio buttons ── */
[data-testid="stRadio"] label { font-size: 0.9rem !important; }
[data-testid="stRadio"] > div { gap: 1rem; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e9ecef !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #adb5bd;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid #e9ecef;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def format_duration(seconds):
    if not seconds:
        return "Unknown"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s" if h else f"{m}m {s}s"


def format_size(bytes_val):
    if not bytes_val:
        return "Unknown"
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} TB"


def is_valid_url(url):
    platforms = [
        r"instagram\.com",
        r"facebook\.com|fb\.watch",
        r"tiktok\.com",
        r"twitter\.com|x\.com",
        r"reddit\.com",
        r"vimeo\.com",
        r"dailymotion\.com",
        r"twitch\.tv",
        r"soundcloud\.com",
        r"spotify\.com",
    ]
    pattern = r"(https?://)?(www\.)?(" + "|".join(platforms) + r")/.+"
    return bool(re.match(pattern, url.strip()))


def fetch_info(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extractor_args": {"youtube": ["player_client=ios,android"]},
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def get_formats(info):
    formats = []
    seen = set()

    # Video+audio formats
    for f in info.get("formats", []):
        if f.get("vcodec") != "none" and f.get("acodec") != "none":
            res = f.get("height")
            if res and res not in seen:
                seen.add(res)
                formats.append({
                    "label": f"{res}p (Video + Audio)",
                    "format_id": f["format_id"],
                    "height": res,
                    "filesize": f.get("filesize") or f.get("filesize_approx"),
                    "ext": f.get("ext", "mp4"),
                    "type": "video",
                })

    # Best video-only qualities
    for f in info.get("formats", []):
        if f.get("vcodec") != "none" and f.get("acodec") == "none":
            res = f.get("height")
            label = f"{res}p HD (Video only)" if res else "Video only"
            if label not in seen:
                seen.add(label)
                formats.append({
                    "label": label,
                    "format_id": f"{f['format_id']}+bestaudio",
                    "height": res or 0,
                    "filesize": f.get("filesize") or f.get("filesize_approx"),
                    "ext": "mp4",
                    "type": "video",
                })

    # Audio only
    formats.append({
        "label": "Audio Only (MP3)",
        "format_id": "bestaudio/best",
        "height": -1,
        "filesize": None,
        "ext": "mp3",
        "type": "audio",
    })

    formats.sort(key=lambda x: x["height"], reverse=True)
    return formats


def download_video(url, fmt, progress_bar, status_text):
    tmpdir = tempfile.mkdtemp()
    output_path = os.path.join(tmpdir, "%(title)s.%(ext)s")
    downloaded_file = [None]

    def progress_hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                pct = downloaded / total
                progress_bar.progress(min(pct, 1.0))
                status_text.markdown(
                    f'<p style="color:#7a766e;font-size:0.82rem;">'
                    f'Downloading… {format_size(downloaded)} / {format_size(total)}</p>',
                    unsafe_allow_html=True,
                )
        elif d["status"] == "finished":
            downloaded_file[0] = d["filename"]
            status_text.markdown(
                '<p style="color:#ff3c00;font-size:0.82rem;">Processing…</p>',
                unsafe_allow_html=True,
            )

    ydl_opts = {
        "format": fmt["format_id"],
        "outtmpl": output_path,
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": ["player_client=ios,android"]},
    }

    if fmt["type"] == "audio":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        # Only use merge_output_format for video if not using format merging
        if "+" not in fmt["format_id"]:
            ydl_opts["merge_output_format"] = "mp4"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        error_str = str(e)
        if "ffmpeg" in error_str.lower() or "merge" in error_str.lower():
            status_text.empty()
            raise Exception("FFmpeg is missing! High-quality downloads require FFmpeg to merge video and audio streams. Please install it and add it to your system PATH.")
        else:
            raise

    # Find the actual output file
    for f in Path(tmpdir).iterdir():
        if f.is_file():
            return str(f)

    return downloaded_file[0]


# ── Session state ─────────────────────────────────────────────────────────────
if "video_info" not in st.session_state:
    st.session_state.video_info = None
if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-title">
  <span class="hero-accent">MEDIA</span><br>DOWN<br>LOADER
</div>
<p class="hero-sub" style="font-size: 0.85rem; line-height: 1.6;">
  <b>Supported Platforms:</b> Instagram • TikTok • X (Twitter) • Facebook • Reddit • Vimeo • SoundCloud • Spotify • Twitch • Dailymotion
</p>
<hr class="red-line">
""", unsafe_allow_html=True)

# URL Input
url = st.text_input(
    "Media URL",
    placeholder="https://www.instagram.com/p/... or https://www.tiktok.com/...",
    key="url_input",
)

col1, col2 = st.columns([3, 1])

with col1:
    fetch_btn = st.button("▶  FETCH VIDEO INFO", use_container_width=True)

with col2:
    clear_btn = st.button("✕  CLEAR", use_container_width=True)

if clear_btn:
    st.session_state.video_info = None
    st.session_state.file_bytes = None
    st.session_state.file_name = None
    st.rerun()

# ── Fetch info ─────────────────────────────────────────────────────────────────
if fetch_btn:
    if not url:
        st.error("Please enter a media URL.")
    elif "youtube" in url.lower() or "youtu.be" in url.lower():
        st.error("YouTube downloads are unsupported to ensure the app's server stability.")
    elif not is_valid_url(url):
        st.error("Platform not supported. Try Instagram, TikTok, Twitter, Facebook, etc.")
    else:
        with st.spinner("Fetching video info…"):
            try:
                info = fetch_info(url)
                st.session_state.video_info = info
                st.session_state.file_bytes = None
                st.session_state.file_name = None
            except Exception as e:
                st.error(f"Could not fetch video: {e}")

# ── Show video info & download options ────────────────────────────────────────
if st.session_state.video_info:
    info = st.session_state.video_info

    # Thumbnail
    thumb = info.get("thumbnail")
    if thumb:
        st.image(thumb, use_container_width=True)

    # Info card
    duration = format_duration(info.get("duration"))
    uploader = info.get("uploader") or info.get("channel") or "Unknown"
    view_count = info.get("view_count")
    views_str = f"{view_count:,}" if view_count else "N/A"

    st.markdown(f"""
    <div class="info-card">
        <div class="title">{info.get('title', 'Untitled')}</div>
        <div class="meta">
            <span>Channel:</span> {uploader} &nbsp;·&nbsp;
            <span>Duration:</span> {duration} &nbsp;·&nbsp;
            <span>Views:</span> {views_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Format selector
    formats = get_formats(info)
    format_labels = [f["label"] for f in formats]
    selected_label = st.selectbox("FORMAT", format_labels, key="fmt_select")
    selected_fmt = next(f for f in formats if f["label"] == selected_label)

    # File size hint
    if selected_fmt.get("filesize"):
        st.markdown(
            f'<p style="font-size:0.8rem;color:#7a766e;margin-top:-0.5rem;">'
            f'Estimated size: <span style="color:#aaa">{format_size(selected_fmt["filesize"])}</span></p>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Download button
    dl_btn = st.button("⬇  DOWNLOAD", use_container_width=True)

    if dl_btn:
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            filepath = download_video(url, selected_fmt, progress_bar, status_text)
            progress_bar.progress(1.0)

            if filepath and os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    st.session_state.file_bytes = f.read()
                st.session_state.file_name = os.path.basename(filepath)
                status_text.markdown(
                    '<p style="color:#ff3c00;font-size:0.9rem;font-weight:600;">✓ Ready to save!</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.error("Download completed but file not found. Try a different format.")
        except Exception as e:
            st.error(f"Download failed: {e}")
            progress_bar.empty()

    # Save-to-disk button
    if st.session_state.file_bytes and st.session_state.file_name:
        st.download_button(
            label=f"💾  SAVE  —  {st.session_state.file_name}",
            data=st.session_state.file_bytes,
            file_name=st.session_state.file_name,
            mime="video/mp4" if not st.session_state.file_name.endswith(".mp3") else "audio/mpeg",
            use_container_width=True,
        )

# ── How-to expander ────────────────────────────────────────────────────────────
with st.expander("HOW TO USE"):
    st.markdown("""
    1. **Paste** a media URL (Instagram, TikTok, Facebook, Twitter, etc.) into the field above.
    2. Click **Fetch Video Info** to preview the media.
    3. Choose your preferred **format / quality**.
    4. Click **Download** — the file will be prepared on the server.
    5. Click **Save** to download the file to your device.

    **Supported Platforms:**
    - Instagram (Reels, Posts, Stories)
    - TikTok
    - Facebook (Videos, Reels)
    - Twitter/X
    - Reddit
    - Vimeo
    - SoundCloud

    > 🚫 **Note on YouTube**: YouTube links are purposely blocked in this app to prevent server IP bans and guarantee stability for other platforms.

    > ⚠️ Only download content you have the right to use.  
    > This tool is intended for personal, offline viewing of media you own or have permission to download.
    """)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Built with yt-dlp &amp; Streamlit · Multi-platform downloader · For personal use only</div>', unsafe_allow_html=True)
