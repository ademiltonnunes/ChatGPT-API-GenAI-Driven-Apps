import os
import openai
import sys
sys.path.append('../..')

#PDF
from langchain.document_loaders import PyPDFLoader
#Split document
from langchain.text_splitter import RecursiveCharacterTextSplitter
#Embedding
from langchain.embeddings.openai import OpenAIEmbeddings
#Vectorstores
import shutil
from langchain.vectorstores import Chroma
#ChatBot
# from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']
persist_directory = 'docs/chroma/'

class LangChaing:

    def __load_PDF(self, pathPdf:str):    
        pdf = PyPDFLoader(pathPdf)
        return pdf.load()

    def __split_content(self, docs):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1500,
            chunk_overlap = 150
        )

        return text_splitter.split_documents(docs)

    def __create_vectorstore(self, chunks):       
        #Create Indexes
        embedding = OpenAIEmbeddings()

        # Remove the directory and its contents
        if os.path.exists(persist_directory):
            directory_path = f'./{persist_directory}'
            shutil.rmtree(directory_path)

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory=persist_directory
        )
     
    def upload_file(self, path):
        pdf_directory = path

        docs = []
        pdf_files = []
        for f in os.listdir(pdf_directory):
            if f.endswith('.pdf'):
                pdf_files.append(f)
        
        if len(pdf_files) > 0:

            for pdf in pdf_files:
                file_path = f"{path}/{pdf}"
                docs.extend(self.__load_PDF(file_path))
        
        if len(docs) > 0:
            
            #Split chunks
            chunks = self.__split_content(docs)
            
            #Vectorstores
            self.__create_vectorstore(chunks)    

            return True
        else:
            #Since there is not docs to upload, remove possible vectorstore existent
            # Remove the directory and its contents
            if os.path.exists(persist_directory):
                directory_path = f'./{persist_directory}'
                shutil.rmtree(directory_path)

            return False
    
    def __load_chatbot(self, k = 3, chain_type='stuff'):    
        # Directory and file information 
        chroma_filename = 'chroma.sqlite3'    
        chroma_filepath = os.path.join(persist_directory, chroma_filename)

        #Check if directory exist
        if not os.path.exists(persist_directory) and not os.path.isdir(persist_directory):
            raise Exception(f"Error: Directory '{persist_directory}' not found.")
        
        # Check if the vector exists
        if not os.path.exists(chroma_filepath):
            raise Exception(f"Error: Chroma file '{chroma_filepath}' not found.")
        
        # Load the Chroma object from the file
        embedding = OpenAIEmbeddings()
        vector_db = Chroma(persist_directory= persist_directory, embedding_function= embedding)
       
       #Retrieve db        
        retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": k})

       # Create a ConversationBufferMemory
        memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True  # Return chat history as a list of messages
        )

        qa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=False,
            return_generated_question=False,
            memory=memory,
            output_key='answer'  # Specify the desired output key
        )

        return qa

    def chat(self, question):

        try:

            chatbot = self.__load_chatbot()
            response = chatbot({'question': question,'chat_history': []})

            return response
        except Exception as e:
            return e

def main() -> None:
    lc = LangChaing()
    # created = lc.upload_file('LangChain/SFBU_Customer_Support_System/uploads/pdf')
    response = lc.chat("What is SFBU?")
    print(response)

    # chatbot = __load_db(file='LangChain/SFBU_Customer_Support_System/uploads/pdf/2023Catalog.pdf', chain_type='stuff', k=3)

    # response = chatbot({'question': "What is SFBU?",'chat_history': []})

    # print(response)

if __name__ == '__main__':
    main()