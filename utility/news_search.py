import os
import requests

google_news_api = os.environ.get("google_news_api")

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

