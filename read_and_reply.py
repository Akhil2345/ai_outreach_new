import imaplib
import email
from email.mime.text import MIMEText
import smtplib
import time
import csv
import re
from datetime import datetime
import subprocess
from textblob import TextBlob
import ollama
from rich import print


# CONFIGURATION
EMAIL = "email_id"
APP_PASSWORD = "App_Password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"

# 📊 Sentiment Scorer
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

# 🧠 Jaccard Relevance Scorer
def jaccard_similarity(text1, text2):
    def clean_and_tokenize(text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        return set(text.split())

    set1 = clean_and_tokenize(text1)
    set2 = clean_and_tokenize(text2)

    if not set1 or not set2:
        return 0.0

    return round(len(set1 & set2) / len(set1 | set2), 3)

# 📝 Logging
def write_log(email, subject, body, status, time_taken, sentiment, relevance):
    with open("logs/email_log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            email, subject, body, status,
            round(time_taken, 2), sentiment, relevance
        ])
    print(f"📝 Logged: {status} -> {email}")

# 🔁 Main Agent
def main():
    print("🔐 Connecting to Gmail...")
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL, APP_PASSWORD)
    imap.select("inbox")

    status, messages = imap.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    print(f"📥 Found {len(email_ids)} unread emails\n")

    for num in email_ids:
        start_time = time.time()

        res, data = imap.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        from_address = email.utils.parseaddr(msg["From"])[1]
        subject = msg["Subject"]
        print(f"✉️ From: {from_address}")
        print(f"🧾 Subject: {subject}")

        # 🔍 Extract Body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        print(f"📄 Body:\n{body}\n")

        # 🧠 Ask Mistral for Reply
        response = ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': body}]
        )
        reply = response['message']['content']
        print(f"[blue]🧾 Suggested Reply:\n{reply}[/blue]")

        # 🔬 Evaluate Metrics
        sentiment = get_sentiment(reply)
        relevance_score = jaccard_similarity(body, reply)
        print(f"🧠 Relevance Score: {relevance_score}")
        print(f"🎭 Sentiment: {sentiment}\n")

        # 🤖 Ask User
        choice = input("What do you want to do with this reply?\n1. Send as-is  2. Edit  3. Skip\nEnter choice (1/2/3): ").strip()

        if choice == "3":
            print("⏭️ Skipped.")
            write_log(from_address, subject, "Skipped", "Rejected", time.time() - start_time, "N/A", 0.0)
            continue

        if choice == "2":
            with open("temp_reply.txt", "w") as f:
                f.write(reply)
            print("✍️ Edit the file (Ctrl+O to save, Ctrl+X to exit)")
            subprocess.call(["nano", "temp_reply.txt"])
            with open("temp_reply.txt", "r") as f:
                reply = f.read()
            status = "Edited"
        else:
            status = "Sent"

        # 📤 Send Reply
        msg_reply = MIMEText(reply)
        msg_reply["Subject"] = f"Re: {subject}"
        msg_reply["From"] = EMAIL
        msg_reply["To"] = from_address

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, from_address, msg_reply.as_string())
        server.quit()

        print(f"✅ Sent reply to: {from_address}")

        write_log(from_address, subject, reply, status, time.time() - start_time, sentiment, relevance_score)

    imap.logout()
    print("📤 Done. Logged out.")

if __name__ == "__main__":
    main()
