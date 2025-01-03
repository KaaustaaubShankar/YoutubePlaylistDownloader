import streamlit as st
import yt_dlp
import os

def fetch_playlist_info(playlist_url):
    """Fetches information about the playlist."""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'force_generic_extractor': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            return info
    except Exception as e:
        st.error(f"Error fetching playlist info: {e}")
        return None

def download_playlist(playlist_url, download_path):
    """Downloads the playlist as MP3 files to the specified directory."""
    try:
        # Ensure the download path exists
        if not os.path.isdir(download_path):
            os.makedirs(download_path)

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',  # Download best audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convert to MP3
                'preferredquality': '192',  # MP3 quality
            }],
            'quiet': False,  # Show yt_dlp progress
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

        st.success("Download completed!")
    except Exception as e:
        st.error(f"Error downloading playlist: {e}")

# Streamlit App
def main():
    st.title("YouTube Playlist Downloader (MP3 Only)")

    # Step 1: Enter playlist URL
    playlist_url = st.text_input("Enter YouTube Playlist URL:")
    if playlist_url:
        st.write("Fetching playlist details...")
        playlist_info = fetch_playlist_info(playlist_url)

        if playlist_info and 'entries' in playlist_info:
            # Display playlist information
            st.write(f"**Playlist:** {playlist_info.get('title', 'N/A')}")
            st.write(f"**Uploader:** {playlist_info.get('uploader', 'N/A')}")

            # List the first 20 videos in the playlist
            st.write("**Videos in playlist:**")
            for idx, entry in enumerate(playlist_info['entries'][:20]):
                st.write(f"{idx + 1}. {entry['title']}")

            if len(playlist_info['entries']) > 20:
                st.write("... and more")

            # Step 2: Specify download path
            download_path = st.text_input("Specify download directory:", value=os.getcwd())

            # Step 3: Initiate download
            if st.button("Download Playlist"):
                if download_path:
                    st.write(f"Downloading to: `{download_path}`...")
                    download_playlist(playlist_url, download_path)
                else:
                    st.error("Please specify a valid download directory.")
        else:
            st.error("Failed to retrieve playlist details.")

if __name__ == "__main__":
    main()
