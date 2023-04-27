from utility import chat
from utility import search
import streamlit as st

def run_app():
    """
    Run a Streamlit app that takes a user query and returns an improved response using ChatGPT and Google Search.

    The app allows users to provide a query, and it returns an improved response by utilizing ChatGPT
    and Google Search. It uses Streamlit to create a simple web page for user interaction.
    """
    # Set the title of the web page
    st.title("Analyzing Google Search")

    # Create a text input box for users to enter their query
    user_input = st.text_input("Enter your query:")

    # Create a button to trigger the analysis
    if st.button("Analyze"):
        # Call your google_search function with the user input
        google_res_urls = search.google_search(user_input)

        chat_prompt = f"""
        Question is {user_input}
        Assume you're the expert in this area, with 10+ years of experience.
        The websites below provides latest information from google search. Please incorporate those as needed to improve your response. 
        Your response should include 3 sections. 
        First section: Title
        Second section: Summary. You need to provide a summary of your finding upfront, and provide actionable recommendation as needed 
        Third section: 3 bullet points for key insights. 
        No more summary at the end
        Please make the response interesting, concise and self explanatory
        Markdown format with #Headings, ##H3, + bullet points
        websites: {google_res_urls}"""
        result = chat.chat_response(chat_prompt)

        # Display the result on the web page
        st.write(f"Result: {result}")

# Run the Streamlit app
if __name__ == "__main__":
    run_app()

