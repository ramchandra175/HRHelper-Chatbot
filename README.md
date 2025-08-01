# HRHelper – Employee FAQ Chatbot

## Overview
A simple Flask-based chatbot that answers HR FAQs via a web UI and Slack integration.

## Features
- FAQ matching using string similarity.
- Slack Events API integration.
- Web UI interface.
- Logging for unanswered questions.

## Setup Instructions
1. Clone the repo.
2. Run `pip install flask slack_sdk`.
3. Start Flask with `python app.py`.
4. Use ngrok to expose port 5000 and configure Slack with that URL.
5. Update SLACK_BOT_TOKEN in app.py with your real bot token.

## Files
- `app.py`: main backend
- `faq.json`: sample FAQs
- `prompt_log.md`: unanswered questions
- `templates/index.html`: frontend
- `static/script.js`: frontend script
