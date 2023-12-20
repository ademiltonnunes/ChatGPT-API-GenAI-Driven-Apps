import sys
import os
import web_qa

#Openning .env file with api key
with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value
    
# Define API Key
api_key:str = str(os.environ.get("API_KEY"))

# Access command line arguments passed from Node.js
args = sys.argv[1:]

#Generate the question
question = ' '.join(args)

#Answer question
answer = web_qa.Ask(api_key).answerQuestion(question)

print(answer)
