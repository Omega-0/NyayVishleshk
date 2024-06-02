import streamlit as st
import openai
from openai import AzureOpenAI, OpenAI
from streamlit_extras.add_vertical_space import add_vertical_space

def api_session_init():
    if not hasattr(st.session_state,"form_flag"):
        st.session_state.api_key = ""
        st.session_state.model = ""
        st.session_state.version = ""
        st.session_state.type = ""
        st.session_state.endpoint = ""
        st.session_state.form_flag = False

def validate():
    with st.spinner("validating..."):
        if st.session_state.type == "openai":
            if (st.session_state.api_key=="" or st.session_state.endpoint=="" or st.session_state.model==""):
                st.warning("Please enter all credentials")
                return False
            
            else:
                # If credentials are filled verify whether the api is legit or not
                openai.api_key = st.session_state.api_key
                try:
                    client = OpenAI(
                        api_key=st.session_state.api_key,
                        base_url=st.session_state.endpoint,
                    )
                    client.models.list()
                    
                except Exception as e:
                    st.warning(f"Authentication error {e} Please enter correct credentials")
                    return False
                return True
            
        else:
            if (st.session_state.api_key=="" or st.session_state.endpoint=="" or st.session_state.model=="" or st.session_state.version==""):
                st.warning("Please enter all credentials")
                return False
            
            else:
                # If credentials are filled verify whether the api is legit or not
                openai.api_key = st.session_state.api_key
                try:
                    client = AzureOpenAI(
                        api_key=st.session_state.api_key,
                        api_version=st.session_state.version,
                        azure_endpoint=st.session_state.endpoint,
                    )
                    client.models.list()
                    
                except Exception as e:
                    st.warning(f"Authentication error {e} Please enter correct credentials")
                    return False
                st.session_state.form_flag = True
                return True
                
            
def api_form():
    """
    The API Forms update the value of st.session_state.form_flag to True if the api credenitals is successfully validated! It doesn't persist your api credentials.

    To use first init the api_session_init function then utilize the following

    Use st.session_state.form_flag for your code flow
    - `st.session_state.api_key = API Key`
    - `st.session_state.model = Model name`
    - `st.session_state.version = API version`
    - `st.session_state.type = API Type`
    - `st.session_state.endpoint = API endpoint`
    """
    # add_vertical_space(1)
    if st.session_state.form_flag==False:
        
        with st.form("my_form"):
            st.write("Enter your API Credentials")
            checkbox_val = st.radio(label="Choose the type of API",
                                    options=["OpenAI",
                                            "AzureOpenAI"],
                                    horizontal=True)
            
            if checkbox_val=="OpenAI":
                st.session_state.type = "openai"
                st.session_state.api_key = st.text_input("Enter Your API Key")
                st.session_state.endpoint = st.text_input("Enter Your API Endpoint")
                st.session_state.version = st.text_input("API Version", placeholder="Applicable only to AzureOpenAI")
                st.session_state.model = st.selectbox(
                                                        label="Choose your model",
                                                        options=["gpt-3.5-turbo",
                                                                "gpt-4",
                                                                "gpt-4-turbo"],
                                                    
                                                        )
                

            elif checkbox_val=="AzureOpenAI":
                st.session_state.type = "azure"
                st.session_state.api_key = st.text_input("Enter Your API Key")
                st.session_state.endpoint = st.text_input("Enter Your API Endpoint")
                st.session_state.version = st.text_input("API Version", placeholder="Applicable only to AzureOpenAI")
                st.session_state.model = st.selectbox(
                                                        label="Choose your model",
                                                        options=["gpt-3.5-turbo",
                                                                "gpt-4",
                                                                "gpt-4-turbo"]
                                                        )
                st.session_state.model = "gpt-35-turbo" if st.session_state.model=="gpt-3.5-turbo" else st.session_state.model
                
            
            submitted = st.form_submit_button("Submit")

            if submitted and validate():
                st.session_state.form_flag = True
        
                
if __name__== '__main__':
    
    api_form()
    
    # if st.session_state.form_flag:
    #     st.header("Welcome to the app!!")
    #     st.write("API Key - ",st.session_state.api_key)
    #     st.write("Endpoint - ",st.session_state.endpoint)
    #     st.write("Model - ",st.session_state.model)

            


