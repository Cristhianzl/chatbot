import streamlit as st
import requests
import json

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
    "Seja bem vindo ao nosso Chatbot. Faça sua pergunta :)",
)

st.write(
    "Um produto MedCopy.",
)

st.markdown(
    "[www.medcopytool.com/br](https://www.medcopytool.com/br)",
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

LANGFLOW_URL = "https://api.langflow.astra.datastax.com/lf/f0e51f4c-fb9c-4dfe-a815-8e9ce31ee6b0/api/v1/run/2260bcd5-f6a4-46c0-b2b4-a6e07051fc9e"

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
                "Authorization": "Bearer AstraCS:EbweQrmbNseiLSJquyUGlQyy:dfdd3dabb5af7217a4e06f53624cde7c04274bea76a2726782d454b171e66ae3"
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