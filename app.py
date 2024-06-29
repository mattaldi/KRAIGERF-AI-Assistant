import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

st.title("KRAIGERF AI Assistant")

# Get API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env file. Please add it and restart the app.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Set a default model
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call Groq API
def get_groq_response(messages):
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=st.session_state["groq_model"],
            stream=True
        )
        
        for chunk in chat_completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        st.error(f"An error occurred while calling the Groq API: {str(e)}")
        yield "I'm sorry, but I encountered an error while processing your request."

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response_chunk in get_groq_response(st.session_state.messages):
            full_response += response_chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})