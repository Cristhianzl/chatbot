import streamlit as st
import requests
import json

# Show title and description
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Langflow to generate responses. "
)

# Create a session state variable to store the chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Langflow API endpoint
LANGFLOW_URL = "https://api.langflow.astra.datastax.com/lf/f0e51f4c-fb9c-4dfe-a815-8e9ce31ee6b0/api/v1/run/2260bcd5-f6a4-46c0-b2b4-a6e07051fc9e"

def get_langflow_response(messages):
    try:
        # Prepare the payload
        payload = {
            "input_value": messages[-1]["content"] if messages else "",  # Get the last message content
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
        
        # Make the POST request to Langflow
        response = requests.post(
            LANGFLOW_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer AstraCS:EbweQrmbNseiLSJquyUGlQyy:dfdd3dabb5af7217a4e06f53624cde7c04274bea76a2726782d454b171e66ae3"
            }
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        
        # Extract the text from the specific path in the response
        return response_data["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error making request to Langflow: {str(e)}")
        return None
    except (KeyError, IndexError) as e:
        st.error(f"Error parsing Langflow response: {str(e)}")
        return None

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    # Store and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Langflow
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_langflow_response(st.session_state.messages)
            
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})