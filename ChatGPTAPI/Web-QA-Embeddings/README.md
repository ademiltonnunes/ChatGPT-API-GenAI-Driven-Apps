# Web QA Embeddings

This project is a Flask-based implementation of the Web QA Embeddings inspired by a tutorial provided by OpenAI. The tutorial guides you through the process of building an AI system that can answer questions about a website using the OpenAI Embeddings. This implementation uses the tutorial as a foundation and extends it with Flask for a web-based interface.

## Project Overview

### Description

The project involves crawling a website (using the SFBU website as an example), converting the crawled pages into embeddings using the Embeddings API, and implementing a basic search functionality within a web application. Users can then interactively ask questions about the embedded information, providing a foundation for more advanced applications that utilize custom knowledge bases.

### Tutorial Link

For detailed instructions and explanations, refer to the official tutorial: [Web QA Embeddings Tutorial](https://platform.openai.com/docs/tutorials/web-qa-embeddings).

## Getting Started

Follow these steps to set up your project with a virtual environment:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ademiltonnunes/Generative-AI-Driven-Intelligent-Apps-Development.git
 
## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Add your [API key](https://beta.openai.com/account/api-keys) to the `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should be able to access the app at [http://localhost:5000](http://localhost:5000)!
