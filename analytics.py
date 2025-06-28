import csv
from collections import Counter
from rich import print
from rich.table import Table
from statistics import mean

LOG_FILE = "logs/email_log.csv"

def load_logs():
    logs = []
    with open(LOG_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 8:
                logs.append({
                    "timestamp": row[0],
                    "email": row[1],
                    "subject": row[2],
                    "body": row[3],
                    "status": row[4],
                    "time_taken": float(row[5]),
                    "sentiment": row[6],
                    "relevance": float(row[7])
                })
    return logs

def show_dashboard(logs):
    total = len(logs)
    status_count = Counter(log['status'] for log in logs)
    sentiment_count = Counter(log['sentiment'] for log in logs if log['sentiment'] != "N/A")
    times = [log['time_taken'] for log in logs if log['status'] != "Rejected"]
    relevances = [log['relevance'] for log in logs if log['relevance'] > 0]

    avg_time = mean(times) if times else 0
    avg_relevance = mean(relevances) if relevances else 0

    print("\n[bold green]📊 Email Agent Analytics Summary[/bold green]")
    print(f"🧾 Total Emails Processed: [bold]{total}[/bold]")
    print(f"✅ Sent: [cyan]{status_count['Sent']}[/cyan]")
    print(f"📝 Edited: [yellow]{status_count['Edited']}[/yellow]")
    print(f"⏭️ Skipped: [red]{status_count['Rejected']}[/red]")
    print(f"⏱️ Avg Response Time: [bold]{round(avg_time, 2)} sec[/bold]")
    print(f"🧠 Avg Relevance Score: [bold]{round(avg_relevance, 3)}[/bold]")

    if avg_relevance < 0.4:
        print("[red]⚠️ Warning: Low average relevance — AI replies may be off-topic.[/red]")

    print("\n[bold magenta]📈 Sentiment Breakdown[/bold magenta]")
    for sentiment, count in sentiment_count.items():
        pct = round((count / total) * 100, 1)
        print(f"  • {sentiment}: {count} ({pct}%)")

    print("\n[bold magenta]📈 Relevance Score Distribution[/bold magenta]")
    for r in [0.0, 0.3, 0.5, 0.7, 0.9]:
        count = sum(1 for s in relevances if r <= s < r + 0.2)
        print(f"  • {r:.1f} – {r+0.2:.1f}: {count}")

    print("\n[bold cyan]📋 Recent Log Preview:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Email", width=30)
    table.add_column("Status")
    table.add_column("Time (s)")
    table.add_column("Sentiment")
    table.add_column("Relevance")

    for log in logs[-5:]:
        table.add_row(
            log['email'],
            log['status'],
            str(round(log['time_taken'], 1)),
            log['sentiment'],
            str(log['relevance'])
        )
    print(table)

if __name__ == "__main__":
    try:
        logs = load_logs()
        if not logs:
            print("[red]No logs found.[/red]")
        else:
            show_dashboard(logs)
    except FileNotFoundError:
        print("[red]Log file not found. Run the agent first to generate logs.[/red]")
