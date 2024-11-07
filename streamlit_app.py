import streamlit as st
import requests
import json
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LANGFLOW_URL = os.getenv('LANGFLOW_URL')
ASTRA_DB_TOKEN = os.getenv('ASTRA_DB_TOKEN')

# Set page configuration with light theme
st.set_page_config(
    page_title="MedBot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply custom CSS for light theme
st.markdown("""
    <style>
        /* Main app background */
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        /* Chat container */
        .stChatFloatingInputContainer {
            background-color: #FFFFFF !important;
        }
        
        /* Chat messages background */
        .stChatMessage {
            background-color: #F8F9FA !important;
            border: 1px solid #E6E6E6;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }

        /* Target using partial class names */
        div[class*="ea3mdgi6"],
        div[class*="ea3mdgi2"],
        div[class*="message-container"] {
            background-color: #37b366 !important;
        }
            
        /* Force background color for user messages using multiple selectors */
        div[class*="stChatMessage"][class*="user"],
        div[class*="message"][class*="user"],
        div[data-test="user-message"],
        .st-emotion-cache-*[data-test="user-message"] {
            background-color: #37b366 !important;
            color: white !important;
        }

        /* Try targeting with attribute contains */
        div[class*="emotion"][data-test="user-message"],
        div[class*="chat"][data-test="user-message"] {
            background-color: #37b366 !important;
        }
        
        /* User message specific styling */
        .stChatMessage[data-test="user-message"] {
            background-color: #E3F2FD !important;
        }
        
        /* Assistant message specific styling */
        .stChatMessage[data-test="assistant-message"] {
            background-color: #FFFFFF !important;
        }
        
        /* Input box */
        .stChatInputContainer {
            background-color: #FFFFFF !important;
            border-color: #E6E6E6 !important;
        }
        
        /* Text color */
        .stMarkdown {
            color: #2C3E50 !important;
        }
        
        /* Links */
        a {
            color: #1E88E5 !important;
            text-decoration: none;
        }
        
        /* Title */
        .stTitle {
            color: #2C3E50 !important;
        }
        
        /* Center image */
        div[data-testid="stImage"] {
            display: flex;
            justify-content: center;
        }
        
        /* Input area */
        textarea {
            background-color: #FFFFFF !important;
            color: #2C3E50 !important;
        }
        
        /* Chat container background */
        section[data-testid="stChatMessageContainer"] {
            background-color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# Rest of your code remains the same
st.image("https://angular-medcopy.s3.us-east-2.amazonaws.com/medcopySymbol.png", width=200)



st.write(
    "Seja bem vindo ao MedBot",
)


st.markdown(
    "[www.medcopytool.com/br](https://www.medcopytool.com/br)",
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_langflow_response(messages):
    try:
        payload = {
            "input_value": messages[-1]["content"] if messages else "",
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                "ChatInput-Noppm": {},
                "AstraVectorStoreComponent-kKKyc": {},
                "ParseData-QyC2l": {},
                "Prompt-oEZUj": {},
                "ChatOutput-4GRdO": {},
                "OpenAIEmbeddings-xaRbH": {},
                "OpenAIModel-W8yg9": {},
                "note-nZxhu": {},
                "note-mXSOp": {}
            }
        }
        
        response = requests.post(
            LANGFLOW_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ASTRA_DB_TOKEN}"
            }
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        return response_data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request to Langflow: {str(e)}")
        return None
    except (KeyError, IndexError) as e:
        st.error(f"Error parsing Langflow response: {str(e)}")
        return None

# Add a light separator
st.markdown("---")

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Como posso ajudá-lo?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = get_langflow_response(st.session_state.messages)
            
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})