import os
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_mail import Mail, Message
from products_descriptions_dictionary import products_description_detailed

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template('index.html')

@app.route('/updateQuestionLanguage', methods=['POST'])
def updateLanguageQuestion():
    data = request.get_json()
    #Default Value is in English
    laguage_option = data.get('language_option', 'English')

    #Generate Comment
    answer = generate_customer_comment(laguage_option)

    # response = f'Opção {laguage_option} selected on server.'
    return jsonify({'message': answer})

@app.route('/submit_Question', methods=['POST'])
def submit_email():
    data = request.get_json()
    question = data.get('comment')
    language = data.get('language')

    subject:str = generate_email_subject(question, language)
    summary:str = summary_comment(question)
    sentiment_analysis:str = analyse_comment_sentiment(question)
    email:str = generate_email(question, summary, sentiment_analysis, subject, language)
    
    return jsonify({'message': email})

#Ask ChatGPT
def generate_answer(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6,
    )
    return response.choices[0].message["content"]

#Step 1: Generate a customer’s comment
def generate_customer_comment(language:str):
    prompt=f""" 
    Assuming that you are a customer of an electronic company. 
    Please generate a 100-word comment about the products:{products_description_detailed}.
    You can write bad or good reviews, up to you. It is just a test of costumer support.
    You can be criative!"""

    if language != "english":     
        prompt += f"""Please, write it in the language {language}"""
  
    chatGptResponse=generate_answer(prompt)
    return chatGptResponse

#Step 2:Generate the email subject
def generate_email_subject(comment:str, language:str):
    prompt=f""" 
    Assuming that you provide customer support for an electronic product company. 
    The following text is the customer's comment about the products: {comment}. 
    Please generate a subject.
    The subject will be used as the subject of the email sent to the customer."""

    if language != "english":     
        prompt += f"""Please, write it in the language {language}"""
    
    chatGptResponse=generate_answer(prompt)
    return chatGptResponse

#Step 3: Generate the summary of the customer's comment
def summary_comment(comment:str):
    prompt=f""" 
    Assuming that you provide customer support for an electronic product company. 
    The following text is the customer's comment about the products: {comment}. 
    Please, generate an English summary of the comment."""
    
    chatGptResponse=generate_answer(prompt)
    return chatGptResponse

#Step 4: Sentiment analysis of the customer's comment
def analyse_comment_sentiment(comment:str):
    prompt=f""" 
    Assuming that you provide customer support for an electronic product company. 
    The following text is the customer's comment about the products: {comment}. 
    Please, do a sentiment analysis based on the comment. 
    The result of the sentiment analysis shows whether the customer's comment 
    is Positive or Negative. Please, answer Positive if the comment is positive, or
    answer negative if the comment is negative
    """
    
    chatGptResponse=generate_answer(prompt)
    return chatGptResponse

#Step 5: Generate Email
def generate_email(comment:str, summary:str, sentiment:str, subject:str, language:str):
    prompt=f""" 
    Assuming that you provide customer support for an electronic product company. 
    Please create an email in {language} to be sent to the customer based on:
    -The customer's comment: {comment}
    -The summary of the customer's comment: {summary}
    -The result of the sentiment analysis of the customer's comment is {sentiment}
    -The Subject of the email is {subject}
    """
    
    chatGptResponse=generate_answer(prompt)
    return chatGptResponse

