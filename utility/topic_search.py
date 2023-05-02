import requests
import os

url = "https://google-search74.p.rapidapi.com/"
google_search_api = os.environ.get("google_search_api")

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


