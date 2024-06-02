from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, ConversationChain
import os
import streamlit as st
import time
from bot_utility.prompts import master_chain_template
from langchain_core.prompts.prompt import PromptTemplate
from PIL import Image
import regex as re

def get_cache_vectorstore(text_chunks,file_name):
    default_directory = "chroma_custom_store"
    os.makedirs(default_directory,exist_ok=True)
    
    print("Initializing embedding model...")
    embeddings = HuggingFaceInstructEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    ''' if this directory has files
        then use those db directly to created vectorstore and return
        else create new db '''
    
    chroma_directory = os.path.join(default_directory,file_name)
    if not os.path.exists(chroma_directory):
        print("No vectorstore for {} file found creating new vectorstore...".format(file_name))
        os.makedirs(chroma_directory,exist_ok=True)
        
        vectorstore = Chroma.from_texts(texts=text_chunks,embedding=embeddings,persist_directory=chroma_directory)
        print("New Vectorstore created!!!")
        return vectorstore
    
    else:
        print("Existing vectorstore for {} file found...".format(file_name))
        vectorstore = Chroma(persist_directory=chroma_directory, embedding_function=embeddings)
        return vectorstore

def get_text_chunks_from_file(file_path,chunk_size=4000):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=700,
        length_function=len
    )
    chunk_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            # yield text_splitter.split_text(chunk)
            chunk_list.extend(text_splitter.split_text(chunk))
    
    return chunk_list

def get_page_wise_text_chunk(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the regex pattern to match the page delimiters and include them in the result
    pattern = re.compile(r'(page_number_\d+\n.*?\npage_number_\d+\n)', re.DOTALL)

    # Find all matches and return as a list of chunks
    chunks = pattern.findall(content)

    return chunks

def get_vectorstore_openai_emb(text_chunks):
    embeddings = OpenAIEmbeddings(deployment="text-embedding-ada-002")
    vectorstore = Chroma.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

# Preparing Vectorstore
def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

# Retrieving conversational chain
def get_rtr_chain(vectorstore,llm):
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def get_conversation_Chain(llm):
    memory = ConversationBufferMemory()
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=master_chain_template)
    conversation_chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=PROMPT
    )
    return conversation_chain

def doc_to_string(doc):
    refined_content = ""
    for i in range(len(doc)):
        refined_content+=doc[i].page_content
    return refined_content

def perform_vectorsearch(vectorstore,query):
    doc = vectorstore.similarity_search(query)
    ref = doc_to_string(doc)        
    print("len of doc",len(doc))
    return ref

def handle_single_chat(user_ques, master_chain,ipc_vectorstore,bns_vectorstore):
    logo_image = Image.open(r".assests\balance.png",formats=["png"])
    resized_logo = logo_image.resize((10, 10))
    if user_ques:
        with st.chat_message("user"):
            st.write(user_ques)
            
        with st.chat_message("assistant",avatar="⚖️"):
            message_placeholder = st.empty()
            full_response = ""
            message_placeholder.markdown("Thinking..▌")
            
            # Rertrieve the references
            ipc_ref = perform_vectorsearch(ipc_vectorstore,user_ques)
            bns_ref = perform_vectorsearch(bns_vectorstore,user_ques)
            
            final_prompt = "\nIPC Reference \n"+ipc_ref+"\nBNS Reference \n"+bns_ref+f"\nHuman Question - {user_ques}"
            try:
                answer = master_chain.predict(input = final_prompt)
            except Exception as e:
                message_placeholder.markdown("Refreshing my memory..▌")
                master_chain.memory.clear()
                answer = "Please ask the question again."

            print(answer)
            for char in answer:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.005)
            message_placeholder.markdown(full_response)


