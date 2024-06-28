import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Ensure the API key is set in the environment
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Initialize the GoogleGenerativeAI model
model = GoogleGenerativeAI(model='gemini-1.0-pro')

# Helper function to display and send Streamlit messages
def llm_function(model, query):
    if query.startswith("Hello"):
        output = "Hey there! How can I assist you today?"
    else:
        response = model.invoke(query)
        output = response  # Assuming the response is the output itself


    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

st.title("Gemini Explorer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and load chat history
for index, message in enumerate(st.session_state.messages):
    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# For initial message startup
if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive"
    llm_function(model, initial_prompt)

# Capture user input
query = st.text_input("Gemini Explorer")

# If user input is provided, personalize ReX's responses
if query:
    llm_function(model, query)
