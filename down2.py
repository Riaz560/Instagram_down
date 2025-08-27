# app.py
import streamlit as st
import instaloader
import os
import tempfile
import time
import random
from pathlib import Path

# ---------- secrets ----------
IG_USERNAME = st.secrets["riazarif19288"]
IG_PASSWORD = st.secrets["2580"]
SESSION_FILE = ".instaloader-session"

# ---------- helper ----------
@st.cache_resource(show_spinner=False)
def get_loader():
    """
    Log in (once per app lifetime) and return an authenticated Instaloader.
    """
    loader = instaloader.Instaloader(
        user_agent=(
            "Mozilla/5.0 (Linux; Android 11; SM-G975F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.6422.14 Mobile Safari/537.36"
        )
    )

    if Path(SESSION_FILE).exists():
        loader.load_session_from_file(IG_USERNAME)
        return loader

    loader.login(IG_USERNAME, IG_PASSWORD)
    loader.save_session_to_file(SESSION_FILE)
    return loader

def download_reel(url: str):
    try:
        # extract shortcode
        for marker in ("/reel/", "/p/"):
            if marker in url:
                shortcode = url.split(marker)[1].split("/")[0]
                break
        else:
            return None, "Invalid URL"

        loader = get_loader()
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # small jitter to avoid rate-limit
        time.sleep(random.uniform(1, 2))

        with tempfile.TemporaryDirectory() as tmp:
            loader.download_post(post, target=tmp)
            mp4_files = [f for f in os.listdir(tmp) if f.endswith(".mp4")]
            if not mp4_files:
                return None, "No video found"

            with open(os.path.join(tmp, mp4_files[0]), "rb") as f:
                return f.read(), f"{shortcode}.mp4"

    except Exception as e:
        return None, str(e)

# ---------- UI ----------
st.set_page_config(page_title="IG Reel Downloader", page_icon="📥")
st.title("📥 Instagram Reel Downloader")
st.markdown("Download public Instagram Reels to your device.")

url = st.text_input("Paste the Reel URL here:")

if st.button("Download"):
    if url:
        with st.spinner("Fetching video…"):
            data, name = download_reel(url)
            if data:
                st.success("✅ Done!")
                st.download_button(
                    label="Save .mp4",
                    data=data,
                    file_name=name,
                    mime="video/mp4",
                )
            else:
                st.error(name)
    else:
        st.warning("Please enter a URL first.")

st.markdown("---")
st.caption("For personal use only. Respect Instagram’s Terms.")
    if not IG_USERNAME or not IG_PASSWORD:
        raise RuntimeError(
            "Instagram credentials not found. "
            "Set IG_USERNAME / IG_PASSWORD as environment variables "
            "or in Streamlit Secrets."
        )

    loader.login(IG_USERNAME, IG_PASSWORD)
    loader.save_session_to_file(SESSION_FILE)
    return loader

# ---------- DOWNLOAD ----------
def download_reel(reel_url: str):
    try:
        # Extract shortcode
        for token in ["/reel/", "/p/"]:
            if token in reel_url:
                shortcode = reel_url.split(token)[-1].split("/")[0]
                break
        else:
            return None, "Invalid Instagram Reel URL"

        # Login once per app run (cached)
        if "loader" not in st.session_state:
            st.session_state.loader = get_logged_in_loader()

        loader = st.session_state.loader
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Rate-limit
        time.sleep(random.uniform(1, 2))

        with tempfile.TemporaryDirectory() as tmp:
            loader.download_post(post, target=tmp)
            mp4_files = [f for f in os.listdir(tmp) if f.endswith(".mp4")]
            if not mp4_files:
                return None, "MP4 file not found"

            with open(os.path.join(tmp, mp4_files[0]), "rb") as fh:
                return fh.read(), f"reel_{shortcode}.mp4"

    except Exception as e:
        return None, f"Error: {e}"

# ---------- STREAMLIT UI ----------
st.set_page_config(
    page_title="Instagram Reel Downloader",
    page_icon="📥",
    layout="centered"
)

st.title("📥 Instagram Reel Downloader")
st.markdown("Download public Instagram Reels anonymously after a one-time login.")

reel_url = st.text_input(
    "Instagram Reel URL:",
    placeholder="https://www.instagram.com/reel/XXXXXX/"
)

if st.button("Download"):
    if reel_url:
        with st.spinner("Downloading …"):
            video_bytes, filename_or_error = download_reel(reel_url)
            if video_bytes:
                st.success("✅ Download complete!")
                st.download_button(
                    label="Save video",
                    data=video_bytes,
                    file_name=filename_or_error,
                    mime="video/mp4"
                )
            else:
                st.error(filename_or_error)
    else:
        st.warning("Please enter a valid Instagram Reel URL.")

st.markdown("---")
st.markdown("**Instructions:**")
st.markdown("1. Open the desired Reel on Instagram.")
st.markdown("2. Copy its URL from the address bar.")
st.markdown("3. Paste above and click **Download**.")

st.caption(
    "For personal use only. Respect Instagram’s Terms of Service."
)
