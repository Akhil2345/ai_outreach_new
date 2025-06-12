import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
from ollama import chat

EMAIL = "akhil627283@gmail.com"
APP_PASSWORD = "hrbjdnrkboscfocu"

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()
    return ""

print("Connecting to Gmail IMAP...")
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL, APP_PASSWORD)
print("Logged in successfully.")

imap.select("inbox")
print("Inbox selected.")

status, messages = imap.search(None, 'UNSEEN')
email_ids = messages[0].split()

print(f"Found {len(email_ids)} unread emails.")

for e_id in email_ids:
    print("\nFetching email ID:", e_id.decode())
    res, msg_data = imap.fetch(e_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = decode_header(msg["Subject"])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode()

    from_address = email.utils.parseaddr(msg.get("From"))[1]
    print("From:", from_address)
    print("Subject:", subject)

    body = get_email_body(msg)
    print("Body received:\n", body)

    print("Sending body to Mistral (via Ollama)...")
    mistral_response = chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are an assistant replying to emails."},
            {"role": "user", "content": body}
        ]
    )

    reply_text = mistral_response["message"]["content"]
    print("Generated reply:\n", reply_text)

    print("Connecting to Gmail SMTP...")
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(EMAIL, APP_PASSWORD)

    reply = MIMEText(reply_text)
    reply["Subject"] = f"Re: {subject}"
    reply["From"] = EMAIL
    reply["To"] = from_address

    print("Sending reply email...")
    smtp.sendmail(EMAIL, from_address, reply.as_string())
    smtp.quit()
    print("Reply sent to:", from_address)

imap.logout()
print("Logged out of Gmail.")

