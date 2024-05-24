# Customer Support System - Questions and Answers

This project is a Flask-based implementation aiming to create a customer support assistant system that answers customer questions about products available to be bought in an electronic store. The system provides responses to customers' inquiries.

## Deep Learning Course: Building Systems with the ChatGPT API

This project employs techniques from the "Building Systems with the ChatGPT API" course by deeplearning.ai, available at [Building Systems with the ChatGPT API](https://learn.deeplearning.ai/chatgpt-building-system/lesson/1/introduction).

## Techniques for Answering Questions

To address client questions about store products, the following techniques taught in the course were employed:
- **Check Customer Questions Techniques:**
  - **Moderation**: Utilize the moderation API to check inappropriate user messages. The system usage must be responsible and avoid abuses. OpenAI's Moderation tool ensures that it is used in compliance with OpenAI policies. Moderation is maintained between user and assistant roles.
  - **Prompt Injection Prevention**: Implement a mechanism to prevent prompt injection. Users may attempt to trick or manipulate the system to answer inappropriate questions or reveal private sensitive information.
- **Analyzing Customer’s Questions:**
  - **Classification**: Classify customer queries to generate different responses based on the question. For example, if a comment is from a specific department in the electronic store, it correctly classifies it. A comment can be directed to different departments simultaneously. Distinguishing each department is responsible for solving a problem or answering a question.
- **Improve Requests Techniques:** 
  - **Chain of Thought Reasoning**: A strategy to guide the model through the process in steps. It allows the model to think before providing answers, breaking down complex tasks into a series of reasoning steps.
- **Fine-tuning:** 
  - **Check Output**: Before retrieving the output, check its answer. Check inappropriate answers with moderation and incorrect answers through self-evaluation.

## Key Features

- Integration with the ChatGPT OpenAI GPT-3.5 model for automatic response generation.
- User interface built with HTML and CSS for easy interaction.

## Technologies Used

- Flask: Web framework for efficient application implementation.
- HTML and CSS: Creating a user-friendly and intuitive interface.
- ChatGPT OpenAI GPT-3.5: Advanced language model for generating contextual responses.

## Getting Started

Follow these steps to set up your project with a virtual environment:

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

   ```bash
   git clone https://github.com/ademiltonnunes/ChatGPT-API-GenAI-Driven-Apps.git

3.  Navigate into the project directory
      ```bash
        cd Customer-Support-System-Q-and-A

5. Create a new virtual environment:

   ```bash
   python -m venv venv
   ```
6. Active the new virtual environment:
   - Linux:
    ```bash
      . venv/bin/activate
     ```
   - Windows:
   ```bash
   .\venv\Scripts\Activate
    ```
7. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

8. Add your [API key](https://beta.openai.com/account/api-keys) to the `.env` file.

9. Run the app:

   ```bash
   flask run
   ```

You should be able to access the app at [http://localhost:5000](http://localhost:5000)!

## Usage
Once the Flask application is running, you can use the web interface to ask question related to store product's and get answers.
