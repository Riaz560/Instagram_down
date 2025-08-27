import streamlit as st
import instaloader
import os
import shutil
import tempfile

def download_reel(reel_url):
    try:
        # Extract shortcode from URL
        if "/reel/" in reel_url:
            shortcode = reel_url.split("/reel/")[-1].split("/")[0]
        elif "/p/" in reel_url:
            shortcode = reel_url.split("/p/")[-1].split("/")[0]
        else:
            return None, "Invalid Instagram Reel URL"

        # Initialize Instaloader
        loader = instaloader.Instaloader()

        # Fetch the Reel
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Create a temporary directory to download the reel
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the Reel to the temporary directory
            loader.download_post(post, target=temp_dir)

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
st.caption("এই টুলটি শুধুমাত্র ব্যক্তিগত ব্যবহারের জন্য। Instagram এর terms of service মেনে ব্যবহার করুন。")            return None, "Video URL not found in the page"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

def download_video_from_url(video_url):
    """Download video from direct URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(video_url, headers=headers, stream=True)
        response.raise_for_status()
        
        return response.content, None
        
    except Exception as e:
        return None, f"Download error: {str(e)}"

# Streamlit UI
st.set_page_config(
    page_title="Instagram Reel Downloader",
    page_icon="📥",
    layout="centered"
)

st.title("📥 Instagram Reel Downloader")

method = st.radio("Select download method:", ["Instaloader (Recommended)", "Alternative Method"])

reel_url = st.text_input("Instagram Reel URL লিখুন:", placeholder="https://www.instagram.com/reel/CrVqIBOAeeq/")

if st.button("ডাউনলোড করুন"):
    if reel_url:
        with st.spinner("রিল ডাউনলোড হচ্ছে..."):
            if method == "Instaloader (Recommended)":
                video_data, filename = download_reel(reel_url)
            else:
                video_url, filename = extract_video_url(reel_url)
                if video_url:
                    video_data, error = download_video_from_url(video_url)
                    if error:
                        st.error(error)
                else:
                    video_data = None
                    st.error(filename)
            
            if video_data:
                st.success("রিল সফলভাবে ডাউনলোড হয়েছে!")
                st.download_button(
                    label="ভিডিও ডাউনলোড করুন",
                    data=video_data,
                    file_name=filename,
                    mime="video/mp4"
                )
            else:
                st.error("ডাউনলোড ব্যর্থ হয়েছে। দয়া করে কিছুক্ষণ পরে আবার চেষ্টা করুন।")
    else:
        st.warning("দয়া করে একটি বৈধ URL লিখুন।")        # Create a temporary directory to download the reel
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
