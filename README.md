# README

To run this code in render.com we need to create the following environment variables
```yml
TELEGRAM_BOT_TOKEN=
GROQ_API_KEY=
PYTHON_VERSION=3.11.13
```

This app need to be installed on Python 11 environment which supports the older version of  Python Telegram SDK (python-telegram-bot==13.15). For the SDK to work in Flask app, we need an older version of SDK as it is still supports synchronous event. Flask is also an synchronous app. 

Using older version we can demonstrate polling on render.com with simpler code. 