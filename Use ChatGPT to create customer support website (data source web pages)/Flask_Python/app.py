import os
import web_qa
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        question = request.form["question"]
        answer = web_qa.Ask(str(os.getenv("OPENAI_API_KEY"))).answerQuestion(question)
        return redirect(url_for("index", result=answer))

    result = request.args.get("result")
    return render_template("index.html", result=result)
