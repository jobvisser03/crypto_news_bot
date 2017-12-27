import tweepy

consumer_key = 'rIe6nlKs7NqlJlmUdXMe5Hei3'
consumer_secret = 'Q4nrJ5mkViw9e3pp91y8GYmGTdd372yIvba2V3iNJAIoTLGR2s'
access_token = '118662390-X9inf3rdbb9MzH6ZK9v8cus3KQ001m1NXq1QmbxA'
access_token_secret = 'VtMLjQCE5TFqEkvxYbdJLYMA0lQasVOkIeis3E4VwQGvW'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# check title for coin mentions
coins = {'BTC': 'Bitcoin',
         'LTC': 'Litecoin',
         'XRP': 'Ripple',
         'FCT': 'Factom'}

# exclude when
block_words = ['?', 'will', 'Who','Why', 'hype']

# include when
alert_words = ['pump', 'blow', 'bull','grow']

hashtags = ['litecoin', 'ripple', 'iota']

# TODO save reddit or tweet ids to json and check
# TODO when mentions older post, don't do it

# extend with param for: new, rising, hot
def get_tweets():
    hashtags = ['litecoin', 'ripple', 'iota']
    tweets = tweepy.Cursor(api.search, q='litecoin').items(10)
    t_posts = []
    for tweet in tweets:
        txt = tweet.text
        # check title
        has_alert = any(string in txt for string in alert_words)
        has_coins = any(string in txt for string in list(coins.keys()))
        has_block = any(string in txt for string in block_words)

        # TODO extend with not has_block and has_coins
        if not has_alert:
            msg = '[P1-TWITTER] {}'.format(txt)
            t_posts.append(msg)

    return t_posts

# get_tweets()
