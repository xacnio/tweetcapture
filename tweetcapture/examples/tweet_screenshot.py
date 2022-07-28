from tweetcapture import TweetCapture
import asyncio
tweet = TweetCapture()
asyncio.run(tweet.screenshot(
    "https://twitter.com/jack/status/20", "test1.png", mode=3, night_mode=2))
asyncio.run(tweet.screenshot(
    "https://twitter.com/jack/status/20", "test2.png", mode=2, night_mode=2))
asyncio.run(tweet.screenshot(
    "https://twitter.com/jack/status/20", "test3.png", mode=1, night_mode=1))
asyncio.run(tweet.screenshot(
    "https://twitter.com/jack/status/20", "test4.png", mode=0, night_mode=0))
