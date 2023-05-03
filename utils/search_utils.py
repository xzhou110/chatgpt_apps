import os
import requests
from utils.chat_utils import generate_chat_prompt, get_chat_response

url = "https://google-search74.p.rapidapi.com/"
google_search_api = os.environ.get("google_search_api")
google_news_api = os.environ.get("google_news_api")

def search_google(query):
    """
    Perform a Google search and return the top 10 relevant websites.
    
    :param query: A string representing the search query.
    :return: A list of strings representing the URLs of the top 10 search results.
    """
    querystring = {"query": query, "limit": "10", "related_keywords": "true"}

    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": google_search_api,
        "X-RapidAPI-Host": "google-search74.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    
    # Check if the status code indicates a successful response
    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            urls = [x['url'] for x in response_data['results']]
            return urls
        except (ValueError, KeyError):
            print(f"Error: Unable to parse JSON data. Status code: {response.status_code}")
            print("Content:", response.text)
            return []
    else:
        print(f"Error: HTTP request failed with status code {response.status_code}")
        print("Content:", response.text)
        return []


def search_google_news(topic):
    """
    Perform a Google News search and return the top 10 relevant news articles for a given topic.

    :param topic: A string representing the topic to search for.
    :return: A list of strings representing the URLs of the top 10 news articles.
    """
    url = "https://google-news-api1.p.rapidapi.com/search"

    querystring = {
        "language": "en",
        "q": topic,
        "from": "2023-01-01",
        "sort": "date:desc",
        "limit": "10"
    }

    headers = {
        "X-RapidAPI-Key": google_news_api,
        "X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the status code indicates a successful response
    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            urls = [x['link'] for x in response_data['news']['news']]
            return urls
        except (ValueError, KeyError):
            print(f"Error: Unable to parse JSON data. Status code: {response.status_code}")
            print("Content:", response.text)
            return []
    else:
        print(f"Error: HTTP request failed with status code {response.status_code}")
        print("Content:", response.text)
        return []
    
    
def fetch_and_summarize_news(topics):
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
