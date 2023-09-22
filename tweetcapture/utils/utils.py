from re import match
import os
import base64
from PIL import Image, ImageDraw

def is_valid_tweet_url(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?(twitter\.com|x\.com)\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    if result is not None:
        return result[0]
    return False


def get_tweet_file_name(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?(twitter\.com|x\.com)\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    return f"@{result[3]}_{result[5]}_tweetcapture.png"

def get_tweet_base_url(url):
    result = match(
        "^https?:\/\/([A-Za-z0-9.]+)?(twitter\.com|x\.com)\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)", url)
    return f"/{result[3].lower()}/status/{result[5].lower()}"


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



def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im
