import praw
import pprint

reddit_id = '7Z3kvicoZrQG4w'
reddit_secret = 'FmKJUKwwVkEBCIyUHqlSBif87BU'
reddit_app_name = 'crypto_news_bot'

reddit = praw.Reddit(
    client_id=reddit_id,
    client_secret=reddit_secret,
    user_agent='crypto_news_bot:v0.1 (by /u/Kapsalon21)')

# check title for coin mentions
coins = {'BTC': 'Bitcoin',
         'LTC': 'Litecoin',
         'XRP': 'Ripple',
         'FCT': 'Factom'}

# exclude when
block_words = ['?', 'will', 'Who','Why', 'hype']

# include when
alert_words = ['pump', 'blow', 'bull','grow']

# load a dataset with post id's that have already been processed
already_done = []

# Implement streaming logic
subreddit = reddit.subreddit('cryptocurrency')
for submission in subreddit.stream.submissions():
    print(submission.title)

# extend with param for: new, rising, hot
def get_reddit_posts():
    subs = ['Cryptocurrency', 'cryptomarkets', 'altcoin']
    r_posts = []
    for submission in reddit.subreddit('cryptocurrency+cryptomarkets+altcoin').new(limit=100):
        sub_text = submission.selftext.lower()

        # check title
        has_alert = any(string in submission.title for string in alert_words)
        has_coins = any(string in submission.title for string in list(coins.keys()))
        has_block = any(string in sub_text for string in block_words)

        # TODO extend with not has_block and has_coins
        if submission.id not in already_done and not has_block:
            msg = '[P1-REDDIT] {} ({})'.format(submission.title, submission.shortlink)
            r_posts.append(msg)
            already_done.append(submission.id)

    return r_posts


# get_reddit_posts()
