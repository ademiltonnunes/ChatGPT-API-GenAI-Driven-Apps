# Chatbot From Files

This project aims to implement a robust web application for a chatbot that interacts with your personal documents and data, providing responses through semantic search. All responses are specific to the loaded file; if a question is unrelated to the file, the chatbot will not respond. The project also includes a file upload feature that allows users to feed the system with information. It also includes advanced features such as translation, voice recognition, and enhanced user question techniques.

## Deep Learning Course: LangChain Chat with Your Data

This project incorporates techniques from the "LangChain Chat with Your Data" course by deeplearning.ai, available at [LangChain Chat with Your Data](https://learn.deeplearning.ai/langchain-chat-with-your-data/lesson/1/introduction).

## Techniques for Interacting with Your Own Documents and Data in the Chatbot

To interact with documents loaded into the system, the following techniques were employed:

- **Document Loading**: Data can be sourced from various formats including PDFs, websites, databases, and YouTube videos, then converted into text format for system consumption.

- **Splitting Documents**: Once the document is loaded in text format, it is divided into chunks, configurable based on semantic syntax. The project uses the RecursiveCharacterTextSplitter approach and includes Chunk Overlap configuration, influencing the continuity of information.

- **Embedding**: For each chunk, embedding indexes are generated. Semantically closer chunks have similar indexes.

- **Vector Store Database**: Indexes are stored in a vector store database with N dimensions. Semantically neighboring chunks are stored in the same dimensions. The vector store database can be kept in memory or stored locally, easily retrieved for system use.

- **Answering Questions**: The vector store database is used as a basis for answering questions in the LLM. Customer queries draw data from the vector store database, creating a conversational retrieval chain in the LLM.

- **Semantic Search**: Answers are derived through semantic search, employing a nuanced comparison within the vector store. This process involves extracting information by understanding semantic relationships, enhancing the precision and relevance of responses.

- **Conversation Memory Buffer**: Question answering is designed to handle historical questions and context through the Conversation Memory Buffer.

## Key Features
- **Translation**: Integration with Google Translate allows users to chat in multiple languages, enhancing accessibility.
- **Voice Recognition**: Users can ask questions through voice recognition using the Whisper module.
- **Text and Voice Responses**: The system responds in both text and voice, providing a seamless user experience.
- **User Question Techniques**:
  - **Moderation**: OpenAI's Moderation tool ensures responsible usage and compliance with policies.
  - **Prompt Injection Prevention**: Mechanisms are in place to prevent users from injecting inappropriate prompts or revealing sensitive information.
- **Integration with the ChatGPT OpenAI GPT-3.5 model**:  OpenAI GPT-3.5 model is used as a Large Language Model (LLM).
- **User interface built with HTML and CSS** for easy interaction.
- **LangChain** for loading documents, creating a vector store, and answering questions.

## Technologies Used

- Flask: Web framework for efficient application implementation.
- HTML and CSS: Creating a user-friendly and intuitive interface.
- ChatGPT OpenAI GPT-3.5: Advanced language model for the base LLM.
- LangChain for loading documents and answering questions by semantic search in a conversational Memory Buffer.

## Getting Started

Follow these steps to set up your project with a virtual environment:

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

   ```bash
   git clone https://github.com/ademiltonnunes/Generative-AI-Driven-Intelligent-Apps-Development.git

3.  Navigate into the project directory
      ```bash
        cd ChatGPTAPI/Chatbot-From-Files

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
Once the Flask application is running, you can use the web interface to load documents and ask questions related to the personal data uploaded.

Feel free to adjust the content as needed for your specific project requirements!

