
import os
import tweepy
import time

# Load Creds
creds = {}
with open(os.path.expanduser('~/.openclaw/secure/x-credentials.env')) as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            creds[k] = v

client = tweepy.Client(
    consumer_key=creds['TWITTER_API_KEY'],
    consumer_secret=creds['TWITTER_API_SECRET'],
    access_token=creds['TWITTER_ACCESS_TOKEN'],
    access_token_secret=creds['TWITTER_ACCESS_SECRET']
)

handles = [
    "karpathy", "AlexFinn", "openclaw", "steipete", "akshay_pachaar",
    "jsrailton", "thekitze", "OpenRouterAI", "Ambani_Wessley", "callebtc",
    "binghe", "xmayeth", "ItakGol", "Fujin_Metaverse", "iamfra5er",
    "ForrestPKnight", "tankots", "menhguin", "SylvainKalache", "andrewjiang",
    "Ibelick", "bobtabor", "mustafaergisi", "cailynyongyong", "johnbej",
    "Gh0stNnet", "efo_xx", "DaBrusi", "Devinbuild", "Ryanlouder"
]

print(f"Attempting to follow {len(handles)} accounts...")

for handle in handles:
    try:
        # 1. Get User ID
        user = client.get_user(username=handle)
        if not user.data:
            print(f"❌ Could not find user: @{handle}")
            continue
            
        uid = user.data.id
        
        # 2. Follow
        client.follow_user(target_user_id=uid)
        print(f"✅ Followed: @{handle}")
        time.sleep(2) # Safety delay
        
    except Exception as e:
        print(f"❌ Failed @{handle}: {e}")
        if "429" in str(e):
            print("Rate limit hit. Stopping.")
            break
