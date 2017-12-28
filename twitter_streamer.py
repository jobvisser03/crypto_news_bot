from src import twitter_login, slack_login, process_priority, post_to_slack
from src import RTM_READ_DELAY
import time
import tweepy


def main():
    twitter = twitter_login()
    slack_client = slack_login()

    hashtags = ['litecoin', 'ripple', 'iota']

    if slack_client.rtm_connect(with_team_state=False):
        print("Reddit streamer is ready")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        channel = '#crypto-news-bot'
        while True:
            tweets = tweepy.Cursor(twitter.search, q='litecoin').items(10)
            for tweet in tweets:
                item = tweet.text.lower()
                if process_priority(item):
                    print('P1-TWITTER: {}'.format(item))
                    item = 'P1-TWITTER: {}'.format(item)
                    post_to_slack(slack_client, item, channel)
                else:
                    print('P0-TWITTER: {}'.format(item))
                    item = 'P0-TWITTER: {}'.format(item)
                    post_to_slack(slack_client, item, channel)
                time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


if __name__ == '__main__':
    main()
