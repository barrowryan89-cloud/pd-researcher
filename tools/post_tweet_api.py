import os
import tweepy

CREDENTIALS_PATH = os.path.expanduser('~/.openclaw/secure/x-credentials.env')


def load_creds(path):
    creds = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                creds[k.strip()] = v.strip()
    required = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_SECRET'
    ]
    for r in required:
        if r not in creds:
            raise RuntimeError(f'Missing credential: {r}')
    return creds


def post_tweet(text):
    creds = load_creds(CREDENTIALS_PATH)
    auth = tweepy.OAuth1UserHandler(
        creds['TWITTER_API_KEY'],
        creds['TWITTER_API_SECRET'],
        creds['TWITTER_ACCESS_TOKEN'],
        creds['TWITTER_ACCESS_SECRET']
    )
    api = tweepy.API(auth)
    api.update_status(status=text)


def main():
    post_tweet("Sand Street Holdings test post. 🦞")


if __name__ == '__main__':
    main()
