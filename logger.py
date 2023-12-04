# logger.py
def print_header(header_text):
    print(f"\u001b[34m[TwitchClips][INFO]\u001b[0m {header_text}")

def print_error(error_text):
    print(f"\u001b[31m[TwitchClips][ERROR]\u001b[0m {error_text}")

def print_success(success_text):
    print(f"\u001b[32m[TwitchClips][SUCCESS]\u001b[0m {success_text}")
