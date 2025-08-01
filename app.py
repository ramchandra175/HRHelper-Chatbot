from flask import Flask, request, jsonify, render_template
import json
import os
from difflib import SequenceMatcher
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

# Load FAQs from JSON file
with open('faq.json', 'r') as f:
    faqs = json.load(f)

# Slack Bot Token
SLACK_BOT_TOKEN = "xoxb-your-slack-bot-token"
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# File to log unknown questions
LOG_FILE = 'prompt_log.md'

def log_unknown_question(question):
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.utcnow().isoformat()
        f.write(f"- [{timestamp}] Unknown Question: {question}\n")

def find_best_match(user_question):
    best_match = None
    highest_score = 0.0
    for faq in faqs:
        score = SequenceMatcher(None, user_question.lower(), faq['question'].lower()).ratio()
        if score > highest_score:
            highest_score = score
            best_match = faq
    if highest_score >= 0.6:
        return best_match['answer']
    else:
        log_unknown_question(user_question)
        return "Sorry, I don't know the answer to that. I've logged your question for HR to review."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = find_best_match(user_message)
    return jsonify({"answer": reply})

@app.route("/slack", methods=["POST"])
def slack():
    data = request.get_json()
    if data and data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    if data and data.get("event") and "text" in data["event"]:
        user_text = data["event"]["text"]
        reply = find_best_match(user_text)
        channel_id = data["event"]["channel"]
        try:
            slack_client.chat_postMessage(channel=channel_id, text=reply)
        except SlackApiError as e:
            print(f"Slack API error: {e.response['error']}")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
