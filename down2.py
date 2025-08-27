# app.py
import streamlit as st
import instaloader
import os
import tempfile
import time
import random
from pathlib import Path

# ---------- Secrets ----------
IG_USERNAME = st.secrets["IG_USERNAME"]       # ← set in Streamlit Cloud Secrets
IG_PASSWORD = st.secrets["IG_PASSWORD"]
SESSION_FILE = ".instaloader-session"

# ---------- Loader ----------
@st.cache_resource(show_spinner=False)
def get_loader():
    """Return an authenticated Instaloader (cached for whole session)."""
    loader = instaloader.Instaloader(
        user_agent=(
            "Mozilla/5.0 (Linux; Android 11; SM-G975F) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.6422.14 Mobile Safari/537.36"
        )
    )

    if Path(SESSION_FILE).exists():
        loader.load_session_from_file(IG_USERNAME)
        if loader.test_login():
            return loader
        Path(SESSION_FILE).unlink(missing_ok=True)

    if not IG_USERNAME or not IG_PASSWORD:
        raise RuntimeError(
            "Instagram credentials not found. "
            "Add IG_USERNAME and IG_PASSWORD to Streamlit Secrets."
        )

    loader.login(IG_USERNAME, IG_PASSWORD)
    loader.save_session_to_file(SESSION_FILE)
    return loader

# ---------- Download ----------
def download_reel(url: str):
    try:
        for marker in ("/reel/", "/p/"):
            if marker in url:
                shortcode = url.split(marker)[1].split("/")[0]
                break
        else:
            return None, "Invalid Instagram URL"

        loader = get_loader()
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        time.sleep(random.uniform(1, 2))  # small rate-limit delay

        with tempfile.TemporaryDirectory() as tmp:
            loader.download_post(post, target=tmp)
            mp4_files = [f for f in os.listdir(tmp) if f.endswith(".mp4")]
            if not mp4_files:
                return None, "No MP4 found"

            with open(os.path.join(tmp, mp4_files[0]), "rb") as f:
                return f.read(), f"{shortcode}.mp4"

    except Exception as e:
        return None, str(e)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="IG Reel Downloader", page_icon="📥")
st.title("📥 Instagram Reel Downloader")
st.markdown("Paste a public Instagram Reel URL below and press **Download**.")

url = st.text_input("Instagram Reel URL:", placeholder="https://www.instagram.com/reel/XXXXXX/")

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
st.caption("For personal use only. Respect Instagram’s Terms of Service.")
