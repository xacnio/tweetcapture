# Take tweet screenshot and send instagram post or story

from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag, StorySticker
from tweetcapture import TweetCapture
import asyncio
from PIL import Image
import os

IG_USERNAME = "instagram-username-here"
IG_PASSWORD = "instagram-password-here"

cl = None

def upload_story(filename):
    global cl
    if cl is None:
        cl = Client()
        cl.login(IG_USERNAME, IG_PASSWORD)
    story = cl.photo_upload_to_story(
        filename,
    )
    return story

def upload_post_photo(filename, caption=""):
    global cl
    if cl is None:
        cl = Client()
        cl.login(IG_USERNAME, IG_PASSWORD)
    post = cl.photo_upload(
        filename, caption,
    )
    return post

async def main():
    # Tweet Screenshot
    tweet = TweetCapture()
    try:
        path = await tweet.screenshot("https://twitter.com/jack/status/20", "testig.png", mode=3, night_mode=2)
    except Exception as error:
        traceback.print_exc()
        return

    # Convert screenshot image to jpg. Because instagram is accepting jpeg format and screenshot is in png format.
    im1 = Image.open(path)
    jpg_name = path + ".jpg"
    rgb_im = im1.convert('RGB')

    # 1:1 Aspect Ratio / Fit Resize (Instagram Posts not accepting custom aspect ratios)
    # Thanks https://stackoverflow.com/a/2563883
    width, height = im1.size
    rs = max(width, height)
    size = rs, rs
    background_color = (0, 0, 0)
    fit_image = Image.new('RGB', size, background_color)
    bg_w, bg_h = fit_image.size
    offset = ((bg_w - width) // 2, (bg_h - height) // 2)
    fit_image.paste(im1, offset)
    fit_image.save(jpg_name)
    os.remove(path)

    # if jpg is exist, upload
    if os.path.exists(jpg_name):
        upload_story(jpg_name)
        upload_post_photo(jpg_name)

        os.remove(jpg_name)
    else:
        print("convert error")

asyncio.run(main())