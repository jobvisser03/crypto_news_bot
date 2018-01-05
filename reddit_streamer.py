from src import reddit_login, slack_login, process_priority, post_to_slack
from src import RTM_READ_DELAY
import time


def main():
    reddit = reddit_login()
    slack_client = slack_login()

    if slack_client.rtm_connect(with_team_state=False):
        print("Reddit streamer is ready")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        channel = '#crypto-news-bot'
        while True:
            subreddit = reddit.subreddit('cryptocurrency+cryptomarkets+altcoin')
            for submission in subreddit.stream.submissions():
                item = submission.title.lower()
                link = submission.shortlink
                prio_class = process_priority(item)
                item = '{}: {}({})'.format(prio_class, item, link)
                post_to_slack(slack_client, item, channel)
                time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


if __name__ == '__main__':
    main()
