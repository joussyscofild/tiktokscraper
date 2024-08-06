import os
import requests

# Facebook credentials
ACCESS_TOKEN = "EAAOwGHUinK8BO17y3iZBVyefOjZBadAlOwZBKi84zJZACUCqGDli7mUdP1FVBK1kRJeQ2wQxUdjBwZAZC4FJ5f47mJbEVieR6qK2h4DFLZB5NZBV4hbA0suZAZBG1ZAUB7YES63c5zKKBzl1ZA0CFWggvyTILel6mVGguoQYCFjXBRT1MvgP9G0EyMBxVWgpw34E3t4QNvGqBzINA7zsCnueWExDiwdsT6IZD"
PAGE_ID = "101602182578842"
DOWNLOAD_DIR = "downloads"

# Upload video to Facebook
def upload_video_to_facebook(video_path, title, description):
    url = f"https://graph.facebook.com/v12.0/{PAGE_ID}/videos"
    params = {
        'access_token': ACCESS_TOKEN,
        'title': title,
        'description': description
    }
    files = {
        'source': open(video_path, 'rb')
    }
    response = requests.post(url, params=params, files=files)
    return response.json()

# Main function
def main():
    for video_id in os.listdir(DOWNLOAD_DIR):
        video_dir = os.path.join(DOWNLOAD_DIR, video_id)
        if os.path.isdir(video_dir):
            video_path = os.path.join(video_dir, "video.mp4")
            if os.path.exists(video_path):
                title = f"TikTok Video {video_id}"
                description = f"Check out this TikTok video: {video_id}"
                fb_response = upload_video_to_facebook(video_path, title, description)

                if 'id' in fb_response:
                    fb_video_id = fb_response['id']
                    print(f"Uploaded video to Facebook with ID: {fb_video_id}")
                else:
                    print(f"Failed to upload video: {video_path}")
                    print(f"Response: {fb_response}")

if __name__ == "__main__":
    main()
