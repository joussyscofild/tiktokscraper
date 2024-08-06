import http.client
import json
import time
import os
import requests
import subprocess

# Set up RapidAPI credentials
RAPIDAPI_KEY = "5f64efabeamsh7fd76e95df530c1p1431d0jsne5bf537c4868"
RAPIDAPI_HOST = "tiktok-api15.p.rapidapi.com"
DOWNLOAD_DIR = "downloads"
TRACKED_FILE = "downloaded_videos.txt"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Ensure the tracked file exists
if not os.path.exists(TRACKED_FILE):
    open(TRACKED_FILE, 'w').close()

# Load already downloaded video IDs
def load_downloaded_videos():
    with open(TRACKED_FILE, 'r') as file:
        return set(line.strip() for line in file.readlines())

# Save new downloaded video IDs
def save_downloaded_video(video_id):
    with open(TRACKED_FILE, 'a') as file:
        file.write(f"{video_id}\n")

# Download content from a URL
def download_content(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

# Fetch video information
def fetch_videos_by_keyword(keyword, count=10, cursor=0):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    conn.request("GET", f"/index/Tiktok/searchVideoListByKeywords?keywords={keyword}&count={count}&cursor={cursor}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Main function
def main():
    keyword = input("Enter the keyword to search for: ")  # Prompt user for keyword
    num_videos = int(input("Enter the number of videos to scrape: "))  # Prompt user for number of videos
    cursor = 0
    has_more = True
    scraped_count = 0

    downloaded_videos = load_downloaded_videos()

    while has_more and scraped_count < num_videos:
        response = fetch_videos_by_keyword(keyword, count=min(num_videos-scraped_count, 10), cursor=cursor)

        if response.get("code") != 0:
            print(f"Error: {response.get('msg')}")
            break

        videos = response.get("data", {}).get("videos", [])
        cursor = response.get("data", {}).get("cursor", 0)
        has_more = response.get("data", {}).get("hasMore", False)

        for video in videos:
            if scraped_count >= num_videos:
                break

            video_id = video.get("aweme_id")
            if video_id in downloaded_videos:
                continue

            origin_cover_url = video.get("origin_cover")
            play_url = video.get("play")

            if origin_cover_url and play_url:
                # Create a directory for each video
                video_dir = os.path.join(DOWNLOAD_DIR, video_id)
                if not os.path.exists(video_dir):
                    os.makedirs(video_dir)

                origin_cover_path = os.path.join(video_dir, "cover.webp")
                play_path = os.path.join(video_dir, "video.mp4")

                download_content(origin_cover_url, origin_cover_path)
                download_content(play_url, play_path)

                save_downloaded_video(video_id)

                scraped_count += 1
                if scraped_count >= num_videos:
                    break

            time.sleep(2)  # Adding delay to avoid being banned

        if not has_more:
            break
        time.sleep(5)  # Delay before fetching the next batch

    print("Scraping completed. Starting the Facebook upload process...")
    subprocess.run(["python3", "upload_to_facebook.py"])

if __name__ == "__main__":
    main()
