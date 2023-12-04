import requests, json

def get_access_token(CLIENT_ID, CLIENT_SECRET):
    print("\u001b[35m[TwitchClips]\u001b[0m Getting access token from Twitch")

    # Get an access token from Twitch
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        token = response.json()
        access_token = token.get('access_token')

        if access_token:
            print("\u001b[35m[TwitchClips]\u001b[0m Access token received")
            return access_token, token.get('expires_in', 0), token.get('token_type', '')
        else:
            print(f"Error getting access token: {token.get('error', 'Unknown error')}")
    except requests.RequestException as e:
        print(f"Error during access token request: {e}")

    return None, 0, ''  # Return default values if an error occurs