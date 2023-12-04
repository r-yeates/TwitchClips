import os
from opplast import Upload
from logger import print_header, print_error, print_success

def yt_upload(file_name, broadcaster_name, creator_id, subfolder):
    print_header(f"Uploading {file_name} to YouTube...")
    upload = Upload(
        r"YOUR_FIREFOX_PROFILE_PATH",
        headless=True,
        debug=False
    )
    was_uploaded, video_id = upload.upload(
        os.getcwd()+"/"+os.path.join(subfolder, creator_id + "rendered.mp4"),
        title=file_name,
        description=file_name,
        tags=["Twitch", "Clips", "TopClips", "Gaming", f"{broadcaster_name}"]
    )
    if was_uploaded:
        print_success(f"Video uploaded to YouTube - ID: {video_id}")
    else:
        print_error("Video failed to upload to YouTube - ERROR: {upload.error}")
        
    upload.close()