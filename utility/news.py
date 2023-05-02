import os
import requests


google_news_api = os.environ.get("google_news_api")

def search_google_news(topic):

    url = "https://google-news-api1.p.rapidapi.com/search"

    querystring = {"language":"en",
                   "q": topic,
                   "from":"2023-01-01",
                   "sort":"date:desc",
                   "limit":"10"}

    headers = {
        "X-RapidAPI-Key": google_news_api,
        "X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()
    print(response_data)


    # Check if the status code indicates a successful response
    if response.status_code >= 200 and response.status_code < 300:
        try:
            response_data = response.json()
            urls = [x['link'] for x in response_data['news']['news']]
            return urls
        except ValueError:
            print(f"Error: Unable to parse JSON data. Status code: {response.status_code}")
            print("Content:", response.text)
            return []
    else:
        print(f"Error: HTTP request failed with status code {response.status_code}")
        print("Content:", response.text)
        return []

