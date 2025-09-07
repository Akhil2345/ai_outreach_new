# twitter_outreach.py
import os
import csv
import datetime
import ollama
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Load Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)

LOG_FILE = "logs/twitter_log.csv"

def generate_dm(influencer_name, recent_tweet):
    """Use Ollama LLM to generate personalized DM"""
    prompt = f"""
    You are an outreach agent. Draft a short, friendly, professional DM to {influencer_name}.
    Context: They recently tweeted "{recent_tweet}".
    Goal: Invite them for a brand collaboration.
    Keep it under 300 characters. Make it personal and engaging.
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def log_dm(username, message, status):
    """Append DM logs to CSV"""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            username,
            message,
            status
        ])

def find_and_dm(keyword="crypto", limit=5):
    """Find influencers by keyword and DM them"""
    users = api.search_users(q=keyword, count=limit)
    for user in users:
        username = user.screen_name
        recent_tweets = api.user_timeline(screen_name=username, count=1)
        tweet_text = recent_tweets[0].text if recent_tweets else "No recent tweet"

        print(f"\nFound @{username}, generating DM...")
        dm = generate_dm(username, tweet_text)
        print(f"Draft DM:\n{dm}\n")

        choice = input("Send DM? (y/n/edit): ").strip().lower()
        if choice == "y":
            try:
                api.send_direct_message(recipient_id=user.id_str, text=dm)
                log_dm(username, dm, "sent")
                print("✅ DM sent.")
            except Exception as e:
                log_dm(username, dm, f"error: {str(e)}")
                print(f"⚠️ Error sending DM: {e}")
        elif choice == "edit":
            edited_dm = input("Enter your edited DM: ")
            try:
                api.send_direct_message(recipient_id=user.id_str, text=edited_dm)
                log_dm(username, edited_dm, "sent (edited)")
                print("✅ Edited DM sent.")
            except Exception as e:
                log_dm(username, edited_dm, f"error: {str(e)}")
                print(f"⚠️ Error sending edited DM: {e}")
        else:
            log_dm(username, dm, "skipped")
            print("❌ Skipped.")

if __name__ == "__main__":
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        print("❌ Missing Twitter API credentials in .env")
    else:
        find_and_dm(keyword="blockchain", limit=3)
