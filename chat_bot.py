from utils.search_utils import search_google
from utils.chat_utils import generate_chat_prompt, get_chat_response
import streamlit as st

def run_interactive_chatbot():
    """
    Run a Streamlit app that provides improved responses to user queries using ChatGPT and Google Search.

    The app allows users to input a query and receive an improved response by leveraging ChatGPT and Google Search. 
    Streamlit is used to create a user-friendly web interface.
    """
    # Set the title of the web page
    st.title("Interactive Chatbot & Google Search Analyzer")

    # Create a text input box for users to enter their query
    user_input = st.text_input("Enter your query:")

    # Create a button to trigger the analysis
    if st.button("Analyze"):
        input_type = 'question'
        # Call your google_search function with the user input
        google_res_urls = search_google(user_input)
        prompt = generate_chat_prompt(input_type, user_input, google_res_urls)
        result = get_chat_response(prompt)

        # Display the result on the web page
        st.write(result)

run_interactive_chatbot()