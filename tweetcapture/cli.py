import argparse
from tweetcapture import TweetCapture
from asyncio import run
import traceback

def parse_args():
    parser = argparse.ArgumentParser(description='Take a tweet screenshot.')
    parser.add_argument('url', type=str, help="Tweet URL")
    parser.add_argument('-m', "--mode", type=int, help="Mods to show/hide some tweet items (0-4)", default=3)
    parser.add_argument('-t', type=float, help="Waiting time while the page loading (1.0-10.0)", default=5.0)
    parser.add_argument("-n", "--night-mode", type=int, help="Twitter night mode theme (0-2)", default=0)
    parser.add_argument('--lang', type=str,help="Browser language code (tr,en,es,..)", default="")
    parser.add_argument('--chromedriver', type=str, help="Custom chromedriver path", default="")
    parser.add_argument('-o', '--output', type=str, help="Output file name", default="")
    parser.add_argument('-sp', '--show-parent-tweets', dest='show_parent_tweets', action='store_true', help="Show parent tweets")
    parser.add_argument('-sm', '--show-mentions', type=int, help="Show mentions count (default: 0)", default=0)
    parser.add_argument('-r', '--radius', type=int, help="Image radius", default=30)
    parser.add_argument('--overwrite', dest='overwrite', action='store_true', help="Overwrite output file if exists")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help="Debug mode")
    parser.set_defaults(show_parent_tweets=False)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    tweet = TweetCapture(args.mode, args.night_mode, show_parent_tweets=args.show_parent_tweets, show_mentions_count=args.show_mentions, overwrite=args.overwrite, radius=args.radius)
    tweet.set_lang(args.lang)
    tweet.set_wait_time(args.t)
    if len(args.chromedriver) > 0:
        tweet.set_chromedriver_path(args.chromedriver)
    try:
        filename = run(tweet.screenshot(args.url, args.output))
        print(f"Screenshot is saved: {filename}")
    except Exception as error:
        if args.debug:
            traceback.print_exc()
        else:
            print(str(error))
