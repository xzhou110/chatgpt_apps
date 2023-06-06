import openai
import os

openai.api_key = os.environ.get("openai_api")

def generate_chat_prompt(input_type, user_input, article_urls):
    """
    Generate a chat prompt for ChatGPT based on input_type, user_input, and article_urls.

    :param input_type: A string representing the type of input. Possible values include 'question,' 'news,' etc.
    :param user_input: A string representing the user's input query or topic.
    :param article_urls: A list of strings representing the URLs of relevant articles or news from Google Search.
    :return: A string representing the formatted ChatGPT prompt.
    """
    chat_prompt = f"""
                        {input_type}: {user_input}
                        Assume you're an expert in this area, with 10+ years of experience.
                        The websites below provide the latest news, articles, and information from Google Search. Please prioritize newer information and incorporate these as needed to improve your response.

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

                        Websites: {article_urls}
                        """
    return chat_prompt

def get_chat_response(user_prompt):
    """
    Return a ChatGPT response based on a user prompt.
    
    :param user_prompt: A string representing the user's input prompt.
    :return: A string representing the ChatGPT-generated response.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_prompt}]
    )
    return completion.choices[0].message.content
