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
    parser.add_argument('-spl', '--show-parent-limit', type=int, help="Show parent tweets limit (default: -1 = unlimited)", default=-1)
    parser.add_argument('-sm', '--show-mentions', type=int, help="Show mentions count (default: 0)", default=0)
    parser.add_argument('-r', '--radius', type=int, help="Image radius", default=15)
    parser.add_argument('-s', '--scale', type=float, help="Screenshot scale (between 0.0 and 14.0) (1.0 = original, 2.0 = 2x high) (default: 1.0)", default=1.0)

    parser.add_argument('-hp', '--hide-photos', dest='hide_tweet_photos', action='store_true', help="Hide tweet photos")
    parser.add_argument('-hv', '--hide-videos', dest='hide_tweet_videos', action='store_true', help="Hide tweet videos")
    parser.add_argument('-hg', '--hide-gifs', dest='hide_tweet_gifs', action='store_true', help="Hide tweet gifs")
    parser.add_argument('-hq', '--hide-quotes', dest='hide_tweet_quotes', action='store_true', help="Hide tweet quotes")
    parser.add_argument('-hlp', '--hide-link-previews', dest='hide_tweet_link_previews', action='store_true', help="Hide tweet link previews")
    parser.add_argument('-ha', '--hide-all', dest='hide_all_tweet_medias', action='store_true', help="Hide all tweet medias")
    
    parser.add_argument('--overwrite', dest='overwrite', action='store_true', help="Overwrite output file if exists")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help="Debug mode")
    parser.add_argument('--gui', dest='gui', action='store_true', help="GUI mode, open browser window")
    parser.add_argument('--cookies', type=str, help="Set cookies cookie1=value1;cookie2=value2", default="")
    parser.set_defaults(show_parent_limit=-1, show_parent_tweets=False, overwrite=False, debug=False, gui=False, hide_tweet_photos=False, hide_tweet_videos=False, hide_tweet_gifs=False, hide_tweet_quotes=False, hide_tweet_link_previews=False, hide_all_tweet_medias=False)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    tweet = TweetCapture(args.mode, args.night_mode, show_parent_tweets=args.show_parent_tweets, parent_tweets_limit=args.show_parent_limit, show_mentions_count=args.show_mentions, overwrite=args.overwrite, radius=args.radius, scale=args.scale)
    tweet.set_lang(args.lang)
    tweet.set_wait_time(args.t)
    if args.hide_all_tweet_medias is True: 
        tweet.hide_all_media()
    else: 
        tweet.hide_media(args.hide_tweet_link_previews, args.hide_tweet_photos, args.hide_tweet_videos, args.hide_tweet_gifs, args.hide_tweet_quotes)
    tweet.set_gui(args.gui)
    if len(args.chromedriver) > 0:
        tweet.set_chromedriver_path(args.chromedriver)

    if len(args.cookies) > 0:
        cookies = []
        splitted = args.cookies.split(";")
        if len(splitted) >= 1:
            for cookie in splitted:
                cookie = cookie.split("=")
                if len(cookie) == 2:
                    cookies.append({'name': cookie[0], 'value': cookie[1]})
            if len(cookies) > 0:
                tweet.set_cookies(cookies)

    try:
        filename = run(tweet.screenshot(args.url, args.output))
        print(f"Screenshot is saved: {filename}")
    except Exception as error:
        if args.debug:
            traceback.print_exc()
        else:
            print(str(error))
