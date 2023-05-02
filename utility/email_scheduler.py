import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime
import pytz
import search_google_news, generate_chat_prompt, get_chat_response

# Topics for which you want to fetch news articles
topics = ['stock market', 'crypto']

def fetch_and_summarize_news():
    news_summaries = {}

    for topic in topics:
        news_urls = search_google_news(topic)
        summaries = []

        for url in news_urls:
            prompt = generate_chat_prompt('news', topic, [url])
            summary = get_chat_response(prompt)
            summaries.append(summary)

        news_summaries[topic] = summaries

    return news_summaries

def send_email(news_summaries):
    email = os.environ.get('e_add')
    password = os.environ.get('e_pwd')
    to_email = os.environ.get('recipient_e_add')

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email

    current_date = datetime.now().strftime("%b %d, %Y")
    msg['Subject'] = f'{current_date} Daily News Summary'

    body = ''
    for topic, summaries in news_summaries.items():
        body += f"## {topic}\n\n"
        for i, summary in enumerate(summaries):
            body += f"{i + 1}. {summary}\n\n"

    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email, password)
        server.sendmail(email, to_email, text)

def job():
    news_summaries = fetch_and_summarize_news()
    send_email(news_summaries)
    print("News summaries sent!")

# Schedule the job to run daily at 9 AM PST
schedule.every().day.at("00:18").do(job, tz=pytz.timezone('US/Pacific'))

# Keep the script running and executing the scheduled job
while True:
    schedule.run_pending()
    time.sleep(60)