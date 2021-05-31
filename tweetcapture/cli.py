import argparse
from tweetcapture import TweetCapture
from asyncio import run


def parse_args():
    parser = argparse.ArgumentParser(description='Take a tweet screenshot.')
    parser.add_argument('url', type=str, help="Tweet URL")
    parser.add_argument('-m',
                        "--mode", type=int, help="Mods to shpw/hide some tweet items (0-3)", default=0)
    parser.add_argument("-n",
                        "--night-mode", type=int, help="Twitter night mode theme (0-2)", default=0)
    parser.add_argument('--lang', type=str,
                        help="Browser language code (tr,en,es,..)", default="")
    parser.add_argument('--chromedriver', type=str,
                        help="Custom chromedriver path", default="")
    parser.add_argument('-o', '--output', type=str,
                        help="Output file name", default="")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    tweet = TweetCapture(args.mode, args.night_mode)
    tweet.set_browser_lang(args.lang)
    if len(args.chromedriver) > 0:
        tweet.set_chromedriver_path(args.chromedriver)
    filename = run(tweet.screenshot(args.url, args.output))
    print(f"Screenshot is saved: {filename}")
