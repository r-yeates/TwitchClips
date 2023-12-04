import os, requests, datetime
from moviepy.editor import *
from access_token import get_access_token
from yt_upload import yt_upload
from tiktok_upload import tiktok_upload
from logger import print_header, print_error, print_success

# TOUCH THIS ONLY 
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
CLIPS_AMOUNT = 8
# 1 = 24 hours, 7 = 7 days, 30 = 30 days, 90 = 90 days, 180 = 180 days, 365 = 365 days
PERIOD = 1
#GAME_ID = 509658 # Just Chatting, 33214 # Fortnite
GAME_ID = 509658
BROADCASTER_ID = 999
UPLOAD_TO_YOUTUBE = True
UPLOAD_TO_TIKTOK = False

 
# DO NOT TOUCH THIS BELOW

DOWNLOAD_FOLDER = "clips"
CONFIG_FOLDER = "config"
ACCESS_TOKEN_FILE = os.path.join(CONFIG_FOLDER, "access_token.txt")

# Function to load or obtain access token
def get_token():
    try:
        with open(ACCESS_TOKEN_FILE, 'r') as file:
            lines = file.readlines()
            if len(lines) == 2:
                # Check if the access token has expired
                token, seconds_until_expiry = map(str.strip, lines)
                seconds_until_expiry = float(seconds_until_expiry)
                expiry_datetime = datetime.datetime.now() + datetime.timedelta(seconds=seconds_until_expiry)
                current_datetime = datetime.datetime.now() 
                # If the access token has not expired, return it
                if current_datetime < expiry_datetime:
                    return token
                else:
                    print_error("Access token has expired. Obtaining a new one.")
            else:
                print_error("Incorrect format in access token file. Obtaining a new one.")
    except FileNotFoundError:
        print_error("Access token file not found. Obtaining a new one.")

    # Obtain a new access token
    token, seconds_until_expiry, _ = get_access_token(CLIENT_ID, CLIENT_SECRET)
    os.makedirs(CONFIG_FOLDER, exist_ok=True)
    with open(ACCESS_TOKEN_FILE, 'w') as file:
        file.write(f"{token}\n{seconds_until_expiry}")
    return token

# Function to get clips from Twitch
# def get_clips(token):
#     print_header(f"Getting {CLIPS_AMOUNT} clips from Twitch")
#     url = 'https://api.twitch.tv/helix/clips'
#     params = {
#         'game_id': GAME_ID,
#         # 'broadcaster_id': BROADCASTER_ID,
#         'first': CLIPS_AMOUNT + 3, # Add 3 to account for clips that are non English
#         'started_at': f'{datetime.date.today() - datetime.timedelta(days=PERIOD)}T00:00:00Z',
#         'ended_at': f'{datetime.date.today()}T00:00:00Z'
#     }
#     headers = {
#         'Client-ID': CLIENT_ID,
#         'Authorization': f'Bearer {token}'
#     }

#     # Make the request
#     response = requests.get(url, params=params, headers=headers)

#     if response.status_code == 200:
#         print_success(f"Received {CLIPS_AMOUNT} clips from Twitch")
#         return response.json()['data']
#     else:
#         print_error(f'Request failed with status code {response.status_code}')
#         return []

# Function to get clips from Twitch
def get_clips(token):
    print_header(f"Getting {CLIPS_AMOUNT} clips from Twitch")
    url = 'https://api.twitch.tv/helix/clips'
    params = {
        'game_id': GAME_ID,
        'first': CLIPS_AMOUNT + 3,  # Add 3 to account for clips that are non-English
        'started_at': f'{datetime.date.today() - datetime.timedelta(days=PERIOD)}T00:00:00Z',
        'ended_at': f'{datetime.date.today()}T00:00:00Z'
    }
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }

    # Make the request
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        print_success(f"Received {CLIPS_AMOUNT} clips from Twitch")
        clips = response.json()['data']

        # Filter English clips
        english_clips = [clip for clip in clips if clip.get('language', '').lower() == 'en']

        # Use all clips if English clips are less than or equal to CLIPS_AMOUNT
        # Otherwise, use only the first CLIPS_AMOUNT English clips
        selected_clips = english_clips[:CLIPS_AMOUNT] if len(english_clips) > CLIPS_AMOUNT else english_clips

        return selected_clips
    else:
        print_error(f'Request failed with status code {response.status_code}')
        return []

# Function to download a clip
def download_clip(clip, subfolder, file_name):
    thumb = clip['thumbnail_url'].replace('-preview-480x272.jpg', '.mp4')
    clip_response = requests.get(thumb)
    with open(os.path.join(subfolder, clip['creator_id'] + ".mp4"), 'wb') as f:
        for chunk in clip_response.iter_content(chunk_size=1024):
            f.write(chunk)
    print_success(f"Clip Downloaded: {file_name} - Views: {clip['view_count']}")

# Function to process a single clip
def process_clip(clip, downloaded_clips, subfolder):
    # Extract clip information
    title = clip['title']
    url = clip['url']
    creator_name = clip['creator_name']
    broadcaster_name = clip['broadcaster_name']
    thumb = clip['thumbnail_url'].replace('-preview-480x272.jpg', '.mp4')

    file_name = f'{broadcaster_name} - {title}'

    # Check if the clip is already downloaded and rendered
    if os.path.isfile(os.path.join(subfolder, clip['creator_id'] + "rendered.mp4")):
        print_header(f"Clip already downloaded & rendered: {file_name} - Views: {clip['view_count']}")
    else:
        download_clip(clip, subfolder, file_name)
        render_clip(subfolder, clip['creator_id'], file_name, clip, title)  # Pass 'clip' to render_clip

    # Store clip information in the list
    downloaded_clips.append({
        'file_name': file_name,
        'title': title,
        'clip_url': url,
        'creator_name': creator_name,
        'creator_id': clip['creator_id'],
        'broadcaster_name': broadcaster_name,
        'view_count': clip['view_count'],
        'thumb_url': thumb,
        'clip_id': clip['id']
    })

# Function to render a clip
def render_clip(subfolder, creator_id, file_name, clip, title):
    try:
        video = VideoFileClip(os.path.join(subfolder, creator_id + ".mp4"))
        resized_video = video.resize(width=720)
        margined_video = resized_video.margin(top=440, bottom=443, color=(0, 0, 0))

        text = TextClip(title, fontsize=50, color='black', bg_color='white', font='Tahoma-Bold', method='caption', size=(650,None)).set_duration(video.duration).set_position(('center', 250))
        text2 = TextClip(f" Twitch.tv/{clip['broadcaster_name']} ", fontsize=40, color='white', transparent=True, font='Tahoma-Bold').set_duration(video.duration).set_position(('center', 900))
        # image = ImageClip("config/image.png").set_duration(video.duration).set_position(('center', 1000))
        image = VideoFileClip("config/gif.gif").set_duration(video.duration).resize(width=500).set_position(('center', 1000))
        video = CompositeVideoClip([margined_video, text, text2, image])
        video.write_videofile(os.path.join(subfolder, creator_id + "rendered.mp4"), preset='ultrafast', fps=30)
        video.close()
        resized_video.close()
        margined_video.close()
        text.close()
        text2.close()
        image.close()
        print_success(f"Clip Rendered: {file_name} - Deleted original clip")
        os.remove(os.path.join(subfolder, creator_id + ".mp4"))
    except Exception as e:
        print_error(f"Error rendering clip: {e}")

# Main function
def main():
    token = get_token()
    downloaded_clips = []
    subfolder = os.path.join(DOWNLOAD_FOLDER, f'{datetime.date.today()}')
    print_header("Starting TwitchClips...")

    # Ensure download folder exists
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Get clips from Twitch
    clips = get_clips(token)

    # Process each clip
    for clip in clips:
        process_clip(clip, downloaded_clips, subfolder)

    schedule = datetime.datetime.now()
    # Loop through the list of downloaded clips and upload each clip
    for clip_info in downloaded_clips:
        # Upload the clip to YouTube
        if UPLOAD_TO_YOUTUBE:
            yt_upload(clip_info['file_name'], clip_info['broadcaster_name'], clip_info['creator_id'], subfolder)
        else:
            print_header(f"Skipping YouTube upload for {clip_info['file_name']}")
        if UPLOAD_TO_TIKTOK:
            # Upload the clip to TikTok - schedule 25 minutes apart
            schedule = schedule + datetime.timedelta(minutes=25)
            print_header(f"Scheduling TikTok upload for {schedule}")
            tiktok_upload(clip_info['file_name'], clip_info['broadcaster_name'], clip_info['creator_id'], subfolder, schedule)
            # After uploading to YouTube and TikTok, delete the rendered clip
            print_header(f"Deleting rendered clip: {clip_info['file_name']} - Successfuly uploaded")
            os.remove(os.path.join(os.getcwd(), subfolder, clip_info['creator_id'] + "rendered.mp4"))
        else:
            print_header(f"Skipping TikTok upload for {clip_info['file_name']}")

if __name__ == "__main__":
    main()
