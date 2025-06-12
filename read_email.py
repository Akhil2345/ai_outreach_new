import imaplib
import email
from email.header import decode_header

EMAIL = "akhil627283@gmail.com"
APP_PASSWORD = "hrbjdnrkboscfocu"

# Connect to Gmail
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL, APP_PASSWORD)

# Select the inbox
imap.select("inbox")

# Search for unseen (unread) emails
status, messages = imap.search(None, '(UNSEEN)')

# Convert result to list of email IDs
email_ids = messages[0].split()

print(f"\n📬 You have {len(email_ids)} unread emails.\n")

for num in email_ids:
    status, msg_data = imap.fetch(num, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Decode subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    # From field
    from_ = msg.get("From")

    print("📨 From:", from_)
    print("📝 Subject:", subject)
    print("-" * 50)

# Logout
imap.logout()
