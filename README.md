# TweetCapture

Easily take screenshots of tweets/mentions and save them as image.

## Command-Line Usage

```
> pip install tweet-capture
> tweetcapture https://twitter.com/jack/status/20
> tweetcapture -h
```

## Code Usage Examples

- [Test](tweetcapture/tests/test.py)
- [Cli](tweetcapture/cli.py)

## Modes

| #   |                                                   |                                                      |
| --- | ------------------------------------------------- | ---------------------------------------------------- |
| 0   | Hide everything outside tweet content and author. | <img src="tweetcapture/tests/test4.png" width="300"> |
| 1   | Show retweet/like counts.                         | <img src="tweetcapture/tests/test3.png" width="300"> |
| 2   | Show retweet/like counts and timestamp.           | <img src="tweetcapture/tests/test2.png" width="300"> |
| 3   | Show everything.                                  | <img src="tweetcapture/tests/test1.png" width="300"> |

## Night Modes

| #   |            |                                                      |
| --- | ---------- | ---------------------------------------------------- |
| 0   | Light mode | <img src="tweetcapture/tests/test4.png" width="300"> |
| 1   | Dark mode  | <img src="tweetcapture/tests/test3.png" width="300"> |
| 2   | Black mode | <img src="tweetcapture/tests/test1.png" width="300"> |
