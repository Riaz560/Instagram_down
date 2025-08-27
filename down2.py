import streamlit as st
import instaloader
import os
import shutil
import tempfile
from pathlib import Path
import time
import random

# ---------- CONFIG ----------
# 1. Store IG_USERNAME and IG_PASSWORD in Streamlit Secrets (or env vars)
IG_USERNAME = st.secrets.get("riazarif19288") or os.getenv("IG_USERNAME")
IG_PASSWORD = st.secrets.get("2580") or os.getenv("IG_PASSWORD")
SESSION_FILE = ".instaloader-session"  # will be kept in cwd for Streamlit Cloud

# ---------- LOGIN ----------
def get_logged_in_loader() -> instaloader.Instaloader:
    """
    Return an Instaloader instance that is logged in.
    On first run it will create the session file.
    """
    loader = instaloader.Instaloader(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        )
    )

    if Path(SESSION_FILE).exists():
        loader.load_session_from_file(IG_USERNAME)
        if loader.test_login():
            return loader
        # session expired – remove stale file
        Path(SESSION_FILE).unlink(missing_ok=True)

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
