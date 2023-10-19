# Customer Support System: Moderation, Classification, Checkout and Evaluation
## Overview
This project aims to implement a web application of a customer service assistant that answers customer questions about the store's products.
The system was designed as a Flask web application with HTML and CSS user interface. This project used the ChatGPT OpenAI GPT-3.5 Turbo model.
I applied techniques and showed solid examples of Moderation and Prevention of immediate injection in customer queries. Additionally, I checked the customer's response and also checked the AI-generated responses. 
Furthermore, I subjected the system to several test cases and evaluate the system's behavior in all these cases. The system behaved well, despite having to change prompts in some examples. The system generated a different response from a human agent, when compared to responses given by the system and by a human agent.

## Implementation Steps

To run this application, follow these implementation steps:

### 1. Create a Virtual Environment

```bash
python3 -m venv venv bash
```

### 2. Activate the virtual environment:
```bash
. venv/bin/activate
```

### 3.Install the required Python packages:
```bash
pip install flask openai python-dotenv Flask-Mail
```

### 4.Start the Flask application:
```bash
flask run
```

