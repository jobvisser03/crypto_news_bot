import praw
from slackclient import SlackClient
import tweepy
import credentials


def twitter_login():
    auth = tweepy.OAuthHandler(credentials.twitter_consumer_key,
                               credentials.twitter_consumer_secret)
    auth.set_access_token(credentials.twitter_access_token,
                          credentials.twitter_access_token_secret)
    t = tweepy.API(auth)
    return t


def slack_login():
    # instantiate Slack client
    s = SlackClient(credentials.slack_bot_token)
    # starterbot's user ID in Slack: value is assigned after the bot starts up
    # starterbot_id = None
    return s


def reddit_login():
    r = praw.Reddit(
        client_id=credentials.reddit_id,
        client_secret=credentials.reddit_secret,
        user_agent='crypto_news_bot:v0.1 (by /u/Kapsalon21)')
    return r


import requests
import json
r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=1000')
coins = json.loads(r.text)

coin_list = []
for c in coins:
    coin_list.append(c['symbol'].lower())
    coin_list.append(c['id'])

def process_priority(item):

    # exclude when
    block_words = ['?', 'Who', 'Why', 'hype', 'moon', 'top', 'how to',
                   'lambo', 'shill', 'fud', 'hodl', 'pump', 'fees', 'my',
                   'scam', 'developer', 'fomo', 'talk',
                   'dump', 'poloniex', 'picks', 'holding', 'billionaire']

    # include when
    prio_words = ['bull', 'bank', 'next', 'listed', 'announce',
                  'accept', 'release', 'commit', 'deal ', 'consider',
                  'news', 'source code', 'exchange']

    has_prio = any(string in item for string in prio_words)
    # print("Contains priority words: {}".format(has_prio))
    has_coins = any(string in item for string in coin_list)
    # print("Contains coins: {}".format(has_coins))
    has_block = any(string in item for string in block_words)
    # print("Contains block words: {}".format(has_block))

    if has_prio and has_coins:
        return 'PRIO+COIN'
    elif has_block:
        return 'BLOCK'
    elif has_coins:
        return 'COIN'
    else:
        return 'OTHER'


def post_to_slack(s, item, channel):
    s.api_call(
        "chat.postMessage",
        channel=channel,
        text=item
    )
    return True


# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
