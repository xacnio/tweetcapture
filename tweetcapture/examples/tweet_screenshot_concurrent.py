from tweetcapture import TweetCapture
import asyncio

TweetURLs = [
    "https://twitter.com/jack/status/20",
    "https://twitter.com/Twitter/status/1445078208190291973",
    "https://twitter.com/elonmusk/status/1587911540770222081"
]

async def taskCapture(url, port):
    tweet = TweetCapture()
    tweet.add_chrome_argument(f"--remote-debugging-port={port}")
    filename = await tweet.screenshot(url, overwrite=True)
    return filename

async def main():
    PORT = 9222
    TASKS = []
    for url in TweetURLs:
        TASKS.append(asyncio.create_task(taskCapture(url, PORT)))
        PORT += 1

    for task in asyncio.as_completed(TASKS):
        filename = await task
        print(filename)

asyncio.run(main())