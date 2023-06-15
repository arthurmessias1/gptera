import requests
from dotenv import load_dotenv
from flask import Flask, request
import os

load_dotenv('/mnt/d/Projects/Personal/tera_chat_gpt/.env')
app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPEN_AI = os.getenv('OPEN_AI')

def sendmessage(chatid, message):
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {OPEN_AI}"}
    info = {
        # The model used (you can use gpt-4 if you have access to it)
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
        # Randomness of the result
        "temperature": 0.7,
        "max_tokens": 1024
    }
    post_request = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=info)

    response_api = post_request.json()["choices"][0]["message"]["content"]
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "text": response_api,
        "chat_id": chatid
    }
    requests.post(url, json=payload)  # This line is added to send the response back to Telegram


@app.route("/", methods=["POST", "GET"])
def index():
    if (request.method == "POST"):
        resp = request.get_json()
        print(resp)
        # We get the content of the message
        msgtext = resp["message"]["text"]
        # We get the id of the chat
        chatid = resp["message"]["chat"]["id"]
        # The message is sent back
        sendmessage(chatid, msgtext)
        return "Done"
    else:
        return "Hello World!"

if __name__ == "__main__":
    port = 5000
    app.run(debug=True, host='0.0.0.0', port=port)
    
    # send a start-up message
    chat_id = '<your_chat_id>'
    start_message = "Hello, I'm online!"
    sendmessage(chat_id, start_message)
