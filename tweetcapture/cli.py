import argparse
from tweetcapture import TweetCapture
from asyncio import run


def parse_args():
    parser = argparse.ArgumentParser(description='Take a tweet screenshot.')
    parser.add_argument('url', type=str, help="Tweet URL")
    parser.add_argument('-m', "--mode", type=int, help="Mods to shpw/hide some tweet items (0-3)", default=0)
    parser.add_argument("-n", "--night-mode", type=int, help="Twitter night mode theme (0-2)", default=0)
    parser.add_argument('--lang', type=str,help="Browser language code (tr,en,es,..)", default="")
    parser.add_argument('--chromedriver', type=str, help="Custom chromedriver path", default="")
    parser.add_argument('-o', '--output', type=str, help="Output file name", default="")
    parser.add_argument('--fake-name', type=str, help="Fake account name", default="")
    parser.add_argument('--fake-username', type=str, help="Fake account username", default="")
    parser.add_argument('--fake-content', type=str, help="Fake tweet content", default="")
    parser.add_argument('--fake-verified', type=bool, help="Fake tweet verified status", default=False)
    parser.add_argument('--fake-image', type=str, help="Fake account image (url or local file)", default="")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    tweet = TweetCapture(args.mode, args.night_mode)
    tweet.set_lang(args.lang)
    if len(args.chromedriver) > 0:
        tweet.set_chromedriver_path(args.chromedriver)

    if len(args.fake_name) > 0 and len(args.fake_content) > 0:
        tweet.Fake.create(args.fake_name, args.fake_content, args.fake_username, args.fake_image, args.fake_verified)
    filename = run(tweet.screenshot(args.url, args.output))
    print(f"Screenshot is saved: {filename}")
