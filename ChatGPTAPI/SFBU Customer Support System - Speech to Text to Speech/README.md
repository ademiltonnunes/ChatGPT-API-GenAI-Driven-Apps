# SFBU Customer Support System - Speech to Text to Speech
## Overview
This project aims to integrate two projects:

The first project: it is a web application of a customer support system for SFBU that answers customer’s questions based in a loading PDF. This project can be found in: https://github.com/ademiltonnunes/Machine-Learning/tree/main/ChatGPT/Customer%20Support%20System/SFBU%20Customer%20Support%20System%20-%20Chatbot%20From%20Files

The second project: it is implement a AI-Based “Alexa”, which is the possibility of speaking with ChatGPT with voice using Whisper and Google Text to Speech (GTTS). This project can be found in: https://github.com/ademiltonnunes/Machine-Learning/tree/main/ChatGPT/Real-time%20Speech%20to%20Text%20to%20Speech

Please, read the pdf file CS589_week7_q6_19679_AdemiltonMarcelo_DaCruzNunes.pdf. It will have all steps taken to develop this project.

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
pip install python-dotenv
pip install flask
pip install openai
pip install langchain
pip install pydantic==1.10.9
pip install yt_dlp
pip install pydub
pip install pypdf
pip install bs4
pip install tiktoken
pip install langchain[docarray]
pip install chromadb
pip install SpeechRecognition
pip install openai-whisper
pip install gtts
pip install pyaudio
sudo apt install ffmpeg
```

### 4.Start the Flask application:
```bash
flask run
```

