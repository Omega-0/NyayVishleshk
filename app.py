import streamlit as st
import os
from bot_utility.api_form import api_session_init, api_form
from PIL import Image
from bot_utility.htmlTemplates import *
from bot_utility.main import get_page_wise_text_chunk,get_cache_vectorstore,handle_single_chat,get_conversation_Chain,init_chat
from langchain.chat_models import AzureChatOpenAI

if __name__=='__main__':

    # Head Layout
    st.set_page_config(page_title="NyayVishleshak",
    page_icon=r".assests/balance.png",layout="wide")
    
    with st.container():

        # Get the api credentials from user
        api_session_init()
        os.environ["OPENAI_API_TYPE"] = st.session_state.type
        os.environ["OPENAI_API_VERSION"] = st.session_state.version
        os.environ["OPENAI_API_BASE"] = st.session_state.endpoint
        os.environ["OPENAI_API_KEY"] = st.session_state.api_key
        
        # external css
        st.markdown("""
            <style>
                .block-container {
                        padding-top: 3rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
                    .st-emotion-cache-zco55b {
                        position: fixed;
                        bottom: 0px;
                        padding-bottom: 60px;
                        padding-top: 1rem;
                        background-color: rgb(248, 249, 249);
                        z-index: 99;
                    }
                    .st-emotion-cache-4oy321 {
                        display: flex;
                        align-items: flex-start;
                        gap: 0.5rem;
                        padding: 1rem 0px 1rem 1rem;
                        border-radius: 0.5rem;
                        max-height: 300px;
                        overflow: scroll;
                    }
            </style>
            """, unsafe_allow_html=True)
        
        if not hasattr(st.session_state,"executed"):
            st.session_state.executed = True

        with st.container():
            col1,col2,col3=st.columns([0.1,0.8,0.1],gap="large")
            with col1:
                logo_image = Image.open(r".assests/balance.png",formats=["png"])
                resized_logo = logo_image.resize((100, 100))
                # Get the dimensions of the logo image
                logo_width, logo_height = resized_logo.size
                logo= st.image(resized_logo, use_column_width=False, output_format="auto", width=logo_width) 
            with col2:
                # add_vertical_space(1)
                st.title("NyayVishleshak :red[न्यायविश्लेषक]")
                st.subheader("Your bridge between IPC and BNS")

            st.divider()
        st.write(css, unsafe_allow_html=True)

    #API form
    if not st.session_state.form_flag:
        api_form()

    #Main body
    elif st.session_state.form_flag:
        if st.session_state.executed:
            with st.spinner("Intiating Nyayvishlesk..."):
                # get pdf text
                if not hasattr(st.session_state,"vectorstore"): 
                    # get the text chunks
                    ipc_chunks = get_page_wise_text_chunk("referrence_docs/IPC.txt")
                    bns_chunks = get_page_wise_text_chunk("referrence_docs/Bharatiya_Nyaya_Sanhita.txt")

                    # create vector store
                    st.session_state.ipc_vectorstore = get_cache_vectorstore(ipc_chunks,"IPC_Vectorstore")
                    st.session_state.bns_vectorstore = get_cache_vectorstore(bns_chunks,"BNS_Vectorstore")

                    # create conversation chain
                    llm = AzureChatOpenAI(deployment_name = st.session_state.model)
                    st.session_state.master_chain = get_conversation_Chain(llm)
                
                init_chat()
                    
            st.session_state.executed = False              

        # user interaction
        user_question = st.chat_input("Please enter your question here...")                     
        if user_question:
            handle_single_chat(user_question,st.session_state.master_chain,st.session_state.ipc_vectorstore,st.session_state.bns_vectorstore)

            
