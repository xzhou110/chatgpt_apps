# This code is based on a YouTube tutorial I followed as part of a learning course. The original code and concepts belong to the tutorial creator, and
# any modifications or adaptations were made for educational purposes.
# Course Link: https://www.youtube.com/watch?v=-C4FCxP-QqE&t=336s

import openai
import os
import requests
import json
import streamlit as st


openai.api_key = os.environ.get("openai_api_key")
x_rapid_api_key = os.environ.get("x_rapid_api_key")

def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [{"role":"user", "content": userPrompt}]
    )
    return completion.choices[0].message.content


def GetBitCoinPrices():
    
    
    # Define the API endpoint and query parameters
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "7d"
    }
    # Define the request headers with API key and host
    headers = {
        "X-RapidAPI-Key": x_rapid_api_key,
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    # Send a GET request to the API endpoint with query parameters and headers
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    # Parse the response data as a JSON object
    JSONResult = json.loads(response.text)
    # Extract the "history" field from the JSON response
    history = JSONResult["data"]["history"]
    # Extract the "price" field from each element in the "history" array and add to a list
    prices = []
    for change in history:
        prices.append(change["price"])
    # Join the list of prices into a comma-separated string
    pricesList = ','.join(prices)
    # Return the comma-separated string of prices
    return pricesList


bitcoinPrices = GetBitCoinPrices()

chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
                    I will provide you with a list of bitcoin prices for the last 7 days
                    can you provide me with a technical analysis
                    of Bitcoin based on these prices. here is what I want: 
                    Price Overview, 
                    Moving Averages, 
                    Relative Strength Index (RSI),
                    Moving Average Convergence Divergence (MACD),
                    Advice and Suggestion,
                    Do I buy or sell?
                    Please be as detailed as much as you can, and explain in a way any beginner can understand. and make sure to use headings
                    Here is the price list: {bitcoinPrices}"""


if st.button('Analyze'):
    with st.spinner('Getting Bitcoin Prices...'):
        if bitcoinPrices:
            st.success('Done!')
    with st.spinner('Analyzing Bitcoin Prices...'):
        chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
                    I will provide you with a list of bitcoin prices for the last 7 days
                    can you provide me with a technical analysis
                    of Bitcoin based on these prices. here is what I want: 
                    Price Overview, 
                    Moving Averages, 
                    Relative Strength Index (RSI),
                    Moving Average Convergence Divergence (MACD),
                    Advice and Suggestion,
                    Do I buy or sell?
                    Please be as detailed as much as you can, and explain in a way any beginner can understand. and make sure to use headings
                    Here is the price list: {bitcoinPrices}"""
    
        response = BasicGeneration(chatGPTPrompt)
        st.text_area("Analysis", response,
                     height=500)
        st.success('Done!')