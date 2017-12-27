from urllib.parse import quote_plus
import praw
import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient('xoxb-289925568819-4KGqZzmrDz0puWOIqbNjIr4i')
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

QUESTIONS = ['what is', 'who is', 'what are']
REPLY_TEMPLATE = '[Let me google that for you](http://lmgtfy.com/?q={})'

def process_submission(submission, channel):
    # Ignore titles with more than 10 words as they probably are not simple
    # questions.
    if len(submission.title.split()) > 10:
        return

    normalized_title = submission.title.lower()
    for question_phrase in QUESTIONS:
        if question_phrase in normalized_title:
            url_title = quote_plus(submission.title)
            reply_text = REPLY_TEMPLATE.format(url_title)
            print('Replying to: {}'.format(submission.title))
            # print(reply_text)
            slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=reply_text
            )
            # submission.reply(reply_text)
            # A reply has been made so do not attempt to match other phrases.
            break

def get_channel(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        return event["channel"]
    return None

def main():
    reddit_id = '7Z3kvicoZrQG4w'
    reddit_secret = 'FmKJUKwwVkEBCIyUHqlSBif87BU'
    reddit_app_name = 'crypto_news_bot'

    reddit = praw.Reddit(
        client_id=reddit_id,
        client_secret=reddit_secret,
        user_agent='crypto_news_bot:v0.1 (by /u/Kapsalon21)')

    if slack_client.rtm_connect(with_team_state=False):
        print("Google bot is ready")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        channel = '#crypto-news-bot'
        # channel = get_channel(slack_client.rtm_read())
        while True:
            subreddit = reddit.subreddit('AskReddit')
            for submission in subreddit.stream.submissions():
                process_submission(submission, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


if __name__ == '__main__':
    main()
