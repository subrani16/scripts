import pandas as pd
from pytube import Playlist

# --- Configuration ---
PLAYLIST_URL = "YOUTUBE_URL"

def get_playlist_data(playlist_url):
    """
    Fetches video data (title, URL) from a YouTube playlist and returns it as a list of dictionaries.
    """
    try:
        # 1. Create a Playlist object
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title

        print(f"Fetching data for playlist: {playlist_title}")
        print(f"Total videos found: {len(playlist.video_urls)}")

        # 2. Extract video details
        playlist_data = []
        for i, video_url in enumerate(playlist.video_urls):
            # The .videos property is an iterable of all the Video objects in the playlist
            video = playlist.videos[i]

            # Extract basic details
            data = {
                'Index': i + 1,
                'Title': video.title,
                'URL': video.watch_url,
                'Duration (seconds)': video.length,
                'Channel': video.author
            }
            playlist_data.append(data)

        return playlist_data, playlist_title

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def create_pandas_dataframe(data, playlist_title):
    """
    Creates a Pandas DataFrame from the list of video data.
    """
    if data:
        df = pd.DataFrame(data)
        print("\n--- Pandas DataFrame Created Successfully ---")
        print(df.head())

        # Optionally, save the data to a CSV file
        filename = f"{playlist_title.replace(' ', '_').replace('/', '')}_data.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nData saved to CSV file: {filename}")

        return df
    else:
        print("No data to create a DataFrame.")
        return None


if __name__ == "__main__":
    # 1. Get the raw data
    video_data, playlist_name = get_playlist_data(PLAYLIST_URL)

    # 2. Store the data in a Pandas DataFrame
    if video_data:
        df_playlist = create_pandas_dataframe(video_data, playlist_name)
