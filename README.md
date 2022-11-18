# TweetCapture

Easily take screenshots of tweets/mentions and save them as image.

## Command-Line Usage

```
> pip install tweet-capture
> tweetcapture https://twitter.com/jack/status/20
> tweetcapture -h
```

## Code Usage Examples

- [Cli](tweetcapture/cli.py)
- [Code Examples](tweetcapture/examples/)

## Testing
```
> cd tweetcapture/tests/
> python -m unittest
```

## Modes

| #   |                                                   |                                                      |
| --- | ------------------------------------------------- | ---------------------------------------------------- |
| 0   | Hide everything outside tweet content and author. | <img src="tweetcapture/assets/test4.png" width="300"> |
| 1   | Show retweet/like counts.                         | <img src="tweetcapture/assets/test3.png" width="300"> |
| 2   | Show retweet/like counts and timestamp.           | <img src="tweetcapture/assets/test2.png" width="300"> |
| 3   | Show everything.                                  | <img src="tweetcapture/assets/test1.png" width="300"> |
| 4   | Show timestamp.                                   | <img src="tweetcapture/assets/test5.png" width="300"> |

## Night Modes

| #   |            |                                                      |
| --- | ---------- | ---------------------------------------------------- |
| 0   | Light mode | <img src="tweetcapture/assets/test4.png" width="300"> |
| 1   | Dark mode  | <img src="tweetcapture/assets/test3.png" width="300"> |
| 2   | Black mode | <img src="tweetcapture/assets/test1.png" width="300"> |

## Show Mentions Example
_If the tweet have a very many mentions, there may be problems because "show more" option not supported. The tool can show only first loaded mentions. You can limit mention count on screenshot by using -sc <count> argument_
```
tweetcapture -sm 3 https://twitter.com/Twitter/status/1445078208190291973
```
<details>
    <summary>Image</summary>
    <img src="https://i.imgur.com/IZ0GHl8.png" />
</details>

## Show Parent Tweets Example
```
tweetcapture -sp https://twitter.com/elonmusk/status/1587911540770222081
```
<details>
    <summary>Image</summary>
    <img src="https://i.imgur.com/KrK9N8Y.png" />
</details>
