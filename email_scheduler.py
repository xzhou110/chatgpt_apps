import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime, timedelta, time
from time import sleep
import pytz
from utils.search_utils import search_google_news
from utils.chat_utils import generate_chat_prompt, get_chat_response

# Topics for which you want to fetch news articles
topics = ['stock market', 'crypto']

def fetch_and_summarize_news():
    news_summaries = {}

    for topic in topics:
        news_urls = search_google_news(topic)
        summaries = []

        prompt = generate_chat_prompt('news', topic, news_urls)
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
    # Get the current time in the PST timezone
    current_time = datetime.now(pytz.timezone('US/Pacific')).time()

    buffer_minutes = 10  # Buffer to ensure the job will run

    # Check if the current time falls within the buffer range of the scheduled time
    scheduled_time = datetime.time(datetime.combine(datetime.today(), time(scheduled_hour, scheduled_minute)))
    lower_bound = datetime.time(datetime.combine(datetime.today(), scheduled_time) - timedelta(minutes=buffer_minutes))
    upper_bound = datetime.time(datetime.combine(datetime.today(), scheduled_time) + timedelta(minutes=buffer_minutes))

    if lower_bound <= current_time <= upper_bound:
        news_summaries = fetch_and_summarize_news()
        send_email(news_summaries)
        print("News summaries sent!")

# # User-defined scheduling time (in 24-hour format)
# scheduled_hour = 2
# scheduled_minute = 26

# # Schedule the job to run daily at the user-defined time in PST
# scheduled_time = f"{scheduled_hour:02d}:{scheduled_minute:02d}"
# schedule.every().day.at(scheduled_time).do(job)

# # Keep the script running and executing the scheduled job
# while True:
#     schedule.run_pending()
#     sleep(60)


news_summaries = fetch_and_summarize_news()
print(news_summaries)