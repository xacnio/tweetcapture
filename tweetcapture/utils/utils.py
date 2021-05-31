from re import match
import os


def is_valid_tweet_url(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    if result is not None:
        return True
    return False


def get_tweet_file_name(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    return f"@{result[2]}_{result[4]}_tweetcapture.png"

def get_tweet_base_url(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    return f"/{result[2]}/status/{result[4]}"


def get_chromedriver_default_path():
    chrome_driver_env = os.getenv('CHROME_DRIVER')
    if chrome_driver_env is not None:
        return chrome_driver_env
    elif os.name == "nt":
        return "C:/bin/chromedriver.exe"
    else:
        return '/usr/local/bin/chromedriver'
