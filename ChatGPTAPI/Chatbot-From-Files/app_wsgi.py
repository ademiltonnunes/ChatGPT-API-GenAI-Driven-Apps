import os
import openai
from dotenv import load_dotenv
import certifi

# Caminho para o diretório do projeto no PythonAnywhere
project_folder = '/home/ademiltonnnunes/chatbot'

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(project_folder, '.env'))

# Agora você pode acessar as variáveis de ambiente com os.getenv
openai.api_key = os.getenv('OPENAI_API_KEY')

# Certifique-se de que o Python encontra o aplicativo
import sys
sys.path.insert(0, project_folder)

# Importe o aplicativo Flask
from app import app as application

# Inicie o aplicativo Flask
if __name__ == "__main__":
    application.run()