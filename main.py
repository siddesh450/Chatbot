import streamlit as st
from dotenv import load_dotenv
load_dotenv() 
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

## initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to handle input submission
def submit_question():
    input = st.session_state.input_value
    if input:
        response = get_gemini_response(input)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        for chunk in response:
            st.session_state['chat_history'].append(("Bot", chunk.text))
        st.session_state.input_value = ""  # Clear the input field

# Input field with on_change event
input_placeholder = st.empty()
input_placeholder.text_input("Input: ", key="input_value", on_change=submit_question)

# Create a sidebar for chat history
with st.sidebar:
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

st.subheader("The Response is")
for role, text in st.session_state['chat_history']:
    if role == "Bot":
        st.write(text)
