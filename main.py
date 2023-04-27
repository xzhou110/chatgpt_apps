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
    st.title("Interactive Chatbot & Google Search Analyzer")

    # Create a text input box for users to enter their query
    user_input = st.text_input("Enter your query:")

    # Create a button to trigger the analysis
    if st.button("Analyze"):
        # Call your google_search function with the user input
        google_res_urls = search.google_search(user_input)

        chat_prompt = f"""
                        Question: {user_input}
                        Assume you're an expert in this area, with 10+ years of experience.
                        The websites below provide the latest information from Google Search. Please prioritize newer information and incorporate these as needed to improve your response.

                        Your response should include 5 sections:
                        1. ### Title
                        Provide a concise and interesting title that captures the essence of the response.
                        2. #### Summary
                        Give a brief summary of your findings. Always include an actionable recommendation, unless it's inappropriate.
                        3. #### Key Findings
                        - Highlight three key findings from your research, focusing on the most recent and relevant information.
                        4. #### Unique Insights
                        - Share something particularly unique and interesting compared to common understanding on the topic, based on the latest information.
                        5. #### Resources
                        - Include the websites from the Google Search results as resources to support your response, prioritizing up-to-date sources.

                        Please make the response engaging, concise, and self-explanatory.
                        Use Markdown format with ###Headings, ####H4, and - bullet points.

                        Websites: {google_res_urls}
                        """





        result = chat.chat_response(chat_prompt)

        # Display the result on the web page
        st.write(result)

# Run the Streamlit app
if __name__ == "__main__":
    run_app()

