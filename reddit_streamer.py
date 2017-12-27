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
            subreddit = reddit.subreddit('AskReddit')
            for submission in subreddit.stream.submissions():
                item = submission.title.lower()
                if process_priority(item):
                    print('P1-REDDIT: {}'.format(item))
                    post_to_slack(slack_client, item, channel)
                else:
                    print('P0-REDDIT: {}'.format(item))
                time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


if __name__ == '__main__':
    main()
