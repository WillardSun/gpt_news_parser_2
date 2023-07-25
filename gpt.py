import openai
from testing.token_count import num_tokens_from_messages

def askgpt(text, user):
    MODEL = "gpt-3.5-turbo-0613"
    if user.resMode == "positive":
        str = "你能用繁體中文將我提供的新聞裡積極的事情概述嗎\n\n我的新聞：\n" + text
        messages = [
            {"role": "user", "content": str }
        ]
    elif user.resMode == "negative":
        str = "你能用繁體中文將我提供的新聞裡負面的事情概述嗎\n\n我的新聞：\n" + text
        messages = [
            {"role": "user", "content": str }
        ]
    else:
        messages = [
            {"role": "user", "content": "請幫我概述我想要的新聞"},
            {"role": "assistant", "content": "很抱歉，我需要知道你想要的新聞主題和相關信息，才能為你提供一個符合要求的新聞概述。請告訴我你感興趣的新聞主題和更多細節信息。"},
            {"role": "user", "content": text}
        ]
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    responsetxt = ""
    responsetxt += (response['choices'][0]['message']['content'] + '\n')
    responsetxt += (f'Tokens consumed from input: {num_tokens_from_messages(messages)}' + '\n')
    responsetxt += (f'Tokens consumed from output: {response["usage"]["completion_tokens"]}' + '\n')
    return responsetxt