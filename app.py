from flask import Flask, render_template, request
import joblib
from groq import Groq
import os
from telegram.ext import Updater, MessageHandler, Filters

# Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

# Load Telegram bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize Groq client once
groq_client = Groq()

# Global variables for Telegram bot
telegram_app = None
polling_thread = None
updater = None  # Global updater variable

###############################################################
### Function for Telegram bot polling
###############################################################
def handle_message(update, context):
    query = update.message.text
    #print(f"You said: {query}")
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": query
            } # type: ignore
        ]
    )
    #print(f"Bot reply: {completion.choices[0].message.content}")
    update.message.reply_text(completion.choices[0].message.content)
###############################################################


# Initialize Flask app
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    q = request.form.get("q")
    # db
    return(render_template("main.html"))

@app.route("/llama",methods=["GET","POST"])
def llama():
    return(render_template("llama.html"))

@app.route("/llama_reply",methods=["GET","POST"])
def llama_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": q
            } # type: ignore
        ]
    )
    return(render_template("llama_reply.html",r=completion.choices[0].message.content))

@app.route("/deepseek",methods=["GET","POST"])
def deepseek():
    return(render_template("deepseek.html"))

@app.route("/deepseek_reply",methods=["GET","POST"])
def deepseek_reply():
    q = request.form.get("q")
    # load model
    client = Groq()
    completion_ds = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "user",
                "content": q
            } # type: ignore
        ]
    )
    return(render_template("deepseek_reply.html",r=completion_ds.choices[0].message.content))

@app.route("/dbs",methods=["GET","POST"])
def dbs():
    return(render_template("dbs.html"))

@app.route("/prediction",methods=["GET","POST"])
def prediction():
    q = float(request.form.get("q")) # type: ignore
    # load model
    model = joblib.load("dbs.jl")
    # make prediction
    pred = model.predict([[q]])
    return(render_template("prediction.html",r=pred))


###############################################################
### Telegram Flask routes
###############################################################
@app.route("/telegram_polling", methods=["GET", "POST"])
def telegram_polling():
    return render_template("telegram_polling.html", r="Telegram polling not started.")

@app.route("/start_polling", methods=["GET", "POST"])
def start_polling():
    global updater
    if updater is None:
        updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True) # type: ignore
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message)) # type: ignore
        updater.start_polling(drop_pending_updates=True)
        status = "Telegram polling started."
    else:
        status = "Polling already running."
    return render_template("telegram_polling.html", r=status)

@app.route("/stop_polling", methods=["GET", "POST"])
def stop_polling():
    global updater
    if updater:
        updater.stop()
        updater = None
        status = "Telegram polling stopped."
    else:
        status = "Polling was not running."
    return render_template("telegram_polling.html", r=status)
###############################################################

if __name__ == "__main__":
    app.run()

