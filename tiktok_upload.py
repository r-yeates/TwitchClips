import os, datetime
from tiktok_uploader.upload import upload_video
from logger import print_header, print_error, print_success


def tiktok_upload(file_name, broadcaster_name, creator_id, subfolder, schedule):
    upload_video(
        os.getcwd()+"/"+os.path.join(subfolder, creator_id + "rendered.mp4"),
        description=f"{file_name} #Twitch #TwitchClips #Funny #Epic #Fail #TwitchFails #TwitchMoments #TwitchStreamer #Streamer",
        cookies=r'YOUR_COOKIE_PATH',
        schedule=schedule,
        on_complete=lambda : print_success(f"Video uploaded to TikTok"),
        headless=True
    )