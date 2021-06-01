from tweetcapture import TweetCapture
import asyncio
tweet = TweetCapture()
tweet.Fake.create("Elon Musk", "test google.com test #turkishlira test @Twitter test", "@elonmusk", "https://pbs.twimg.com/profile_images/1383184766959120385/MM9DHPWC_200x200.jpg", True)
asyncio.run(tweet.screenshot("", "fake.png", mode=0, night_mode=1))
