import openai
import os

openai.api_key = os.environ.get("openai_api")

def chat_response(user_prompt):
    """
    Return a ChatGPT response based on a user prompt.
    
    :param user_prompt: A string representing the user's input prompt.
    :return: A string representing the ChatGPT-generated response.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_prompt}]
    )
    return completion.choices[0].message.content