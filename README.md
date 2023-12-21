
# TTVClips

TTVClips is a Python script for downloading Twitch clips, rendering them into a 'Tiktok' style format, and uploading them to YouTube and TikTok.


## Installation

Clone the project

```bash
  git clone https://github.com/ryeates/TwitchClips.git
```

Install dependencies

```bash
  pip install -r requirements.txt
```

## Configuration
    1. Obtain Twitch API credentials by creating an application on the Twitch Developer portal.
        a. Set the obtained credentials in the script (replace CLIENT_ID and CLIENT_SECRET in TwitchClips.py).
    2. Download geckodriver and set its path within system environmental variables
    3. Download ImageMagick Display
    4. Setup profile in Firefox for YouTube and copy profile link into TwitchClips.py
    4. Get cookie file (cookies.txt) from TikTok and place it in the config folder
## Preview

![App Screenshot](https://i.imgur.com/IACcsMIm.png)


## License
[MIT License](https://choosealicense.com/licenses/mit/)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

