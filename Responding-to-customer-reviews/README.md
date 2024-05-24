# Responding to Customers Reviews

This project is a Flask-based implementation aiming to create a customer service assistant system for a large electronics store. The system sends email responses to customer product reviews, generating responses based on customer reviews of purchased electronic products.

## Deep Learning Course: ChatGPT Prompt Engineering for Developers

This project employs techniques from the "ChatGPT Prompt Engineering for Developers" course by deeplearning.ai, available at [ChatGPT Prompt Engineering for Developers](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/1/introduction).

## Techniques for Email Response Generation

To generate client responses by email, the following techniques taught in the course were employed:
- **Summarizing**: Summarizing user reviews for brevity.
- **Inferring**: Sentiment classification, topic extraction.
- **Transforming text**: Translation, spelling & grammar correction.
- **Expanding**: Automatically writing emails.

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
        cd Responding-to-customer-reviews

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
Once the Flask application is running, you can use the web interface to generate answers to customers reviews in different languages.

## 

