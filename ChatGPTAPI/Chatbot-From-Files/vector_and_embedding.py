import os
import openai
import sys
import time
sys.path.append('../..')

#PDF
from langchain.document_loaders import PyPDFLoader
#URLs
from langchain.document_loaders import WebBaseLoader
#Youtube
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
#Split document
from langchain.text_splitter import RecursiveCharacterTextSplitter
#Embedding
from langchain.embeddings.openai import OpenAIEmbeddings
#Vectorstores
import shutil
from langchain.vectorstores import Chroma

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']
UPLOAD_FOLDER = 'uploads/pdf'
UPLOAD_URL = 'uploads/url'
UPLOAD_YOUTUBE = 'uploads/youtube'
persist_directory = 'docs/chroma/'
persist_youtube_audio = 'docs/youtube/'
url_file_name = "url.txt"
youtube_file_name = "youtube.txt"

class LangChaing:

    def __load_PDF(self, pathPdf:str):    
        pdf = PyPDFLoader(pathPdf)
        return pdf.load()
    
    def __load_url(self, url:str):
        loader = WebBaseLoader(url)
        return loader.load()

    def __load_youtube(self, url:str):


        loader = GenericLoader(
            YoutubeAudioLoader([url],persist_youtube_audio),
            OpenAIWhisperParser()
        )
        return loader.load()

    def __split_content(self, docs):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1500,
            chunk_overlap = 150
        )

        return text_splitter.split_documents(docs)

    def __create_vectorstore(self, chunks):       
        #Create Indexes
        embedding = OpenAIEmbeddings()

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=persist_directory
        )
    
    def upload_pdf(self, path):
        pdf_path = path

        docs = []       
        docs.extend(self.__load_PDF(pdf_path))
        
        if len(docs) > 0:
            
            #Split chunks
            chunks = self.__split_content(docs)
            
            #Vectorstores
            self.__create_vectorstore(chunks)    

            return True
        else:
            return False
    
    def upload_url(self, url, timer = False):      

        docs = []       
        docs.extend(self.__load_url(url))
        
        if len(docs) > 0:
            
            #Split chunks
            chunks = self.__split_content(docs)
            
            #Vectorstores
            self.__create_vectorstore(chunks)

            if timer:
                time.sleep(10)

            return True
        else:
            return False

    def upload_youtube(self, youtube):      

        docs = []       
        docs.extend(self.__load_youtube(youtube))
        
        if len(docs) > 0:
            
            #Split chunks
            chunks = self.__split_content(docs)
            
            #Vectorstores
            self.__create_vectorstore(chunks)    

            return True
        else:
            return False
    
    def upload_all_files(self):
        #delete vectore
        self.delete_vectorstore()
        
        #Load all files
        pdfs = self.get_pdfs_path()
        urls = self.get_urls()
        youtubes = self.get_youtubes()

        #Load all files existent
        if len(pdfs)>0:
            for pdf in pdfs:
                self.upload_pdf(pdf)
        
        if len(urls)>0:
            for url in urls:
                self.upload_url(url)
        
        if len(youtubes)>0:
            for yt in youtubes:
                self.upload_youtube(yt)

    def get_pdfs_path(self, path = UPLOAD_FOLDER): 

        pdfs_path = []

        for pdf in os.listdir(path):
            if pdf.endswith('.pdf'):
                pdf_path = os.path.join(path, pdf)
                pdfs_path.append(pdf_path)
        
        return pdfs_path
    
    def get_urls(self, path = UPLOAD_URL, url_file = url_file_name):  
        url_links = []
        file_path = os.path.join(path, url_file)
        with open(file_path, 'r') as file:
            url_links = [line.strip() for line in file.readlines()]
        
        return url_links
    
    def get_youtubes(self, path = UPLOAD_YOUTUBE, youtube_file = youtube_file_name):  
        youtube_links = []
        file_path = os.path.join(path, youtube_file)
        with open(file_path, 'r') as file:
            youtube_links = [line.strip() for line in file.readlines()]
        
        return youtube_links
    
    def delete_vectorstore(self, path = persist_directory):
        if os.path.exists(path):
            directory_path = f'./{path}'
            shutil.rmtree(directory_path)

# def main() -> None:
#     lc = LangChaing()
#     # created = lc.upload_file('LangChain/SFBU_Customer_Support_System/uploads/pdf')
    
# if __name__ == '__main__':
#     main()