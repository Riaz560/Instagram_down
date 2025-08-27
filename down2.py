import streamlit as st
import instaloader
import os
import shutil
import tempfile
import time
import random

def download_reel(reel_url):
    try:
        # Extract shortcode from URL
        if "/reel/" in reel_url:
            shortcode = reel_url.split("/reel/")[-1].split("/")[0]
        elif "/p/" in reel_url:
            shortcode = reel_url.split("/p/")[-1].split("/")[0]
        else:
            return None, "Invalid Instagram Reel URL"

        # Initialize Instaloader with custom settings
        loader = instaloader.Instaloader()
        
        # Reduce rate to avoid blocking
        loader.request_timeout = 300
        loader.sleep = True
        loader.sleep_between_requests = 5
        loader.save_metadata = False
        
        # Random delay to avoid detection
        time.sleep(random.uniform(2, 5))

        # Fetch the Reel
        try:
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
        except Exception as e:
            return None, f"Failed to fetch reel: {str(e)}"

        # Create a temporary directory to download the reel
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the Reel to the temporary directory
            try:
                loader.download_post(post, target=temp_dir)
            except Exception as e:
                return None, f"Download failed: {str(e)}"

            # Find the MP4 file
            mp4_file = None
            for filename in os.listdir(temp_dir):
                if filename.endswith(".mp4"):
                    mp4_file = os.path.join(temp_dir, filename)
                    break

            if mp4_file:
                # Read the MP4 file as binary
                with open(mp4_file, 'rb') as f:
                    video_data = f.read()
                
                return video_data, f"reel_{shortcode}.mp4"
            else:
                return None, "MP4 file not found. This might be a private account or the content is not accessible."

    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="Instagram Reel Downloader",
    page_icon="📥",
    layout="centered"
)

st.title("📥 Instagram Reel Downloader")
st.markdown("এই টুলটি ব্যবহার করে আপনি Instagram Reel ডাউনলোড করতে পারবেন।")

# Warning about limitations
st.warning("""
**Note:** Instagram sometimes blocks automated requests. 
If you get an error, please wait a few minutes and try again.
Private accounts cannot be downloaded.
""")

# Input for Instagram Reel URL
reel_url = st.text_input("Instagram Reel URL লিখুন:", placeholder="https://www.instagram.com/reel/CrVqIBOAeeq/")

if st.button("ডাউনলোড করুন"):
    if reel_url:
        with st.spinner("রিল ডাউনলোড হচ্ছে... দয়া করে অপেক্ষা করুন (এটি ১০-৩০ সেকেন্ড সময় নিতে পারে)"):
            video_data, filename = download_reel(reel_url)
            
            if video_data:
                st.success("রিল সফলভাবে ডাউনলোড হয়েছে!")
                
                # Download button
                st.download_button(
                    label="ভিডিও ডাউনলোড করুন",
                    data=video_data,
                    file_name=filename,
                    mime="video/mp4"
                )
            else:
                st.error(filename)
    else:
        st.warning("দয়া করে একটি বৈধ Instagram Reel URL লিখুন。")

st.markdown("---")
st.markdown("**নির্দেশনা:**")
st.markdown("1. Instagram এ আপনার পছন্দের রিল খুলুন")
st.markdown("2. URL কপি করুন (ঠিকানা বারের লিংক)")
st.markdown("3. উপরের বক্সে পেস্ট করুন")
st.markdown("4. 'ডাউনলোড করুন' বাটনে ক্লিক করুন")

# Footer
st.markdown("---")
st.caption("এই টুলটি শুধুমাত্র ব্যক্তিগত ব্যবহারের জন্য। Instagram এর terms of service মেনে ব্যবহার করুন।")                with open(mp4_file, 'rb') as f:
                    video_data = f.read()
                
                return video_data, f"reel_{shortcode}.mp4"
            else:
                return None, "MP4 file not found"

    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="Instagram Reel Downloader",
    page_icon="📥",
    layout="centered"
)

st.title("📥 Instagram Reel Downloader")
st.markdown("এই টুলটি ব্যবহার করে আপনি Instagram Reel ডাউনলোড করতে পারবেন।")

# Input for Instagram Reel URL
reel_url = st.text_input("Instagram Reel URL লিখুন:", placeholder="https://www.instagram.com/reel/CrVqIBOAeeq/")

if st.button("ডাউনলোড করুন"):
    if reel_url:
        with st.spinner("রিল ডাউনলোড হচ্ছে... দয়া করে অপেক্ষা করুন"):
            video_data, filename = download_reel(reel_url)
            
            if video_data:
                st.success("রিল সফলভাবে ডাউনলোড হয়েছে!")
                
                # Download button
                st.download_button(
                    label="ভিডিও ডাউনলোড করুন",
                    data=video_data,
                    file_name=filename,
                    mime="video/mp4"
                )
            else:
                st.error(filename)  # error message
    else:
        st.warning("দয়া করে একটি বৈধ Instagram Reel URL লিখুন।")

st.markdown("---")
st.markdown("**নির্দেশনা:**")
st.markdown("1. Instagram এ আপনার পছন্দের রিল খুলুন")
st.markdown("2. URL কপি করুন (ঠিকানা বারের লিংক)")
st.markdown("3. উপরের বক্সে পেস্ট করুন")
st.markdown("4. 'ডাউনলোড করুন' বাটনে ক্লিক করুন")

# Footer
st.markdown("---")
st.caption("এই টুলটি শুধুমাত্র ব্যক্তিগত ব্যবহারের জন্য। Instagram এর terms of service মেনে ব্যবহার করুন。")
