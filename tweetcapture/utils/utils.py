from re import match
import os
import base64

def is_valid_tweet_url(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    if result is not None:
        return result[0]
    return False


def get_tweet_file_name(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    return f"@{result[2]}_{result[4]}_tweetcapture.png"

def get_tweet_base_url(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    return f"/{result[2].lower()}/status/{result[4].lower()}"


def get_chromedriver_default_path():
    chrome_driver_env = os.getenv('CHROME_DRIVER')
    if chrome_driver_env is not None:
        return chrome_driver_env
    elif os.name == "nt":
        return "C:/bin/chromedriver.exe"
    else:
        return '/usr/local/bin/chromedriver'

def image_base64(filename): 
    if os.path.exists(filename):
        with open(filename, "rb") as image_file:
            encoded_string = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('ascii')
            return encoded_string
    return ""