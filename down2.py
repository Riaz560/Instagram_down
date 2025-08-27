import instaloader
import os
import shutil

def download_reel(reel_url, target_dir):
    # Extract shortcode from URL (e.g., "CrVqIBOAeeq" from ".../reel/CrVqIBOAeeq/")
    shortcode = reel_url.split("/reel/")[-1].split("/")[0]

    # Initialize Instaloader
    loader = instaloader.Instaloader()

    # Optional: Login for private accounts (replace with your credentials)
    # loader.login("USERNAME", "PASSWORD")

    # Fetch the Reel
    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    # Create a temporary directory to download the reel
    temp_dir = f"temp_reel_{shortcode}"
    os.makedirs(temp_dir, exist_ok=True)

    # Download the Reel to the temporary directory
    loader.download_post(post, target=temp_dir)

    # Move the MP4 file to the target directory
    for filename in os.listdir(temp_dir):
        if filename.endswith(".mp4"):
            mp4_file = os.path.join(temp_dir, filename)
            shutil.move(mp4_file, os.path.join(target_dir, f"reel_{shortcode}.mp4"))

    # Remove the temporary directory
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    reel_url = input("Enter Instagram Reel URL: ")
    target_directory = "./"
    os.makedirs(target_directory, exist_ok=True)
    download_reel(reel_url, target_directory)