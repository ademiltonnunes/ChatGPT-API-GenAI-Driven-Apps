# Web QA Embeddings

This project is a Flask-based implementation of the Web QA Embeddings inspired by a tutorial provided by OpenAI. The tutorial guides you through the process of building an AI system that can answer questions about a website using the OpenAI Embeddings. This implementation uses the tutorial as a foundation and extends it with Flask for a web-based interface.

## Project Overview

### Description

The project involves crawling a website (using the SFBU website as an example), converting the crawled pages into embeddings using the Embeddings API, and implementing a basic search functionality within a web application. Users can then interactively ask questions about the embedded information, providing a foundation for more advanced applications that utilize custom knowledge bases.

### Tutorial Link

For detailed instructions and explanations, refer to the official tutorial: [Web QA Embeddings Tutorial](https://platform.openai.com/docs/tutorials/web-qa-embeddings).

## Getting Started

Follow these steps to set up your project with a virtual environment:

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.
   ```bash
   git clone https://github.com/ademiltonnunes/Generative-AI-Driven-Intelligent-Apps-Development.git
 
3. Navigate into the project directory
   ```bash
   cd ChatGPTAPI/Web-QA-Embeddings
 
4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   ```
5. Active the new virtual environment:
   - Linux:
    ```bash
      $ . venv/bin/activate
     ```
   - Windows:
   ```bash
   .\venv\Scripts\Activate
    ```
7. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

8. Add your [API key](https://beta.openai.com/account/api-keys) to the `.env` file.

9. Run the app:

   ```bash
   $ flask run
   ```

You should be able to access the app at [http://localhost:5000](http://localhost:5000)!

## Usage
Once the Flask application is running, you can use the web interface to ask questions about the SFBU website and receive AI-generated answers.

## Personalize to Your Own Website

**Note:** The testing for this project was done on the SFBU website. Due to space constraints, the web crawling of SFBU website was limited only to its the homepage, so this example will answer question only of data present in the homepage. If you want to have questions answered from your own website, you can manually execute the `main()` function in the `web_qa.py` file. Before doing so, make sure to update the `domain` and `full_url` variables with the desired domain and website URL.

Please be aware that the web crawling process can be time-consuming and may cost around $2, depending on the size of the website. In the future, a potential enhancement could involve incorporating the web crawling process into the front-end and limiting the number of websites that can be crawled at once.

