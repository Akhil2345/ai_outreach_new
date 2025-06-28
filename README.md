# 🤖 AI Outreach Agent (Local, Private, LLM-Powered)

An intelligent email automation assistant that reads Gmail inbox, drafts personalized replies using Mistral (via Ollama), and logs everything — with full sentiment analysis, response tracking, and local-first privacy. No API keys. No cloud. 100% offline.

---

## ✨ Key Features

- 📥 Reads unread emails via Gmail IMAP
- 🧠 Generates smart replies using Mistral (local LLM)
- ✍️ Lets you edit replies before sending
- 📤 Sends replies through Gmail SMTP
- 📊 Tracks sentiment (positive/neutral/negative)
- ⏱️ Measures average response time per email
- 🧾 Logs all activity to CSV
- 📈 CLI analytics dashboard to analyze performance
- 🔐 Fully offline and private — no external APIs or data sharing

---

## ⚙️ Tech Stack

| Component       | Tool/Library        |
|-----------------|---------------------|
| LLM             | Mistral via Ollama  |
| Email           | Python (IMAP/SMTP)  |
| Sentiment       | TextBlob            |
| Analytics       | CSV + Rich (Terminal UI) |
| Language        | Python 3.10+        |

---

## 📊 Smart Analytics Included

Every interaction is logged with:
- Sender email
- Subject & timestamp
- Whether reply was sent/edited/skipped
- Time taken to respond
- Sentiment classification (Positive, Neutral, Negative)

### 📈 Example Output:
```
📊 Email Agent Analytics Summary
✅ Emails Processed: 5
📝 Edited: 2 | Sent: 2 | Skipped: 1
⏱ Avg Response Time: 72.4s
📈 Sentiment: 2 Neutral, 2 Positive, 1 Negative
```

You can run analytics anytime using:

```bash
python analytics.py
```

---

## 🚀 Setup Instructions

### 1. Install Ollama + Model
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run mistral
```

---

### 2. Set Up Python Environment
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create `requirements.txt` with:

```
ollama
textblob
rich
```

---

### 3. Gmail Setup

1. Enable **IMAP** in Gmail settings  
2. Turn on **2-Step Verification**  
3. Generate an **App Password**  
4. Add your Gmail + app password into `read_and_reply.py`

---

## ▶️ How to Run

### Start the agent
```bash
python read_and_reply.py
```

- Reads unread emails
- Uses Mistral to generate reply
- Prompts you to:  
  - 1️⃣ Send  
  - 2️⃣ Edit (opens nano)  
  - 3️⃣ Skip  
- Logs everything to `logs/email_log.csv`

---

### Analyze Results Anytime
```bash
python analytics.py
```

You'll see:
- Total replies
- How many were edited/skipped
- Avg response time
- Sentiment breakdown
- Relevance scores (optional if enabled)

---

## 🗂️ Project Structure

```
ai_outreach_new/
├── read_and_reply.py       # Main script to read + reply emails
├── analytics.py            # CLI dashboard for insights
├── logs/
│   └── email_log.csv       # Log file (auto-generated)
├── temp_reply.txt          # Temp file for manual edits
├── requirements.txt
└── README.md
```

---

## 🔮 Future Enhancements

- [ ] Full auto mode (no prompts)
- [ ] CRM logging (Hubspot / Notion API)
- [ ] Export analytics to Google Sheets
- [ ] Web UI via Flask or Streamlit
- [ ] AI memory for smarter follow-ups

---

## 👤 Author

**Akhil Kumar**  
GitHub: [@Akhil2345](https://github.com/Akhil2345)

> Built for productivity, privacy, and measurable insight — powered by open-source AI.
