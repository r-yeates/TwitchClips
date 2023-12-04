# TwitchClips

TwitchClips is a Python script for downloading Twitch clips, rendering them, and uploading them to YouTube and TikTok.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ryeates/TwitchClips.git

2. Install the required dependencies:
    ```
    pip install -r requirements.txt

## Configuration
1. Obtain Twitch API credentials by creating an application on the Twitch Developer portal.
    a. Set the obtained credentials in the script (replace CLIENT_ID and CLIENT_SECRET in TwitchClips.py).
2. Download geckodriver and set its path within system environmental variables
3. Download ImageMagick Display
4. Setup profile in Firefox for YouTube and copy profile link into TwitchClips.py
4. Get cookie file from TikTok and edit tikok_upload.py
