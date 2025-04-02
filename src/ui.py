import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

st.title("🛍️ E-commerce Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
query = st.chat_input("Ask me about products...")
if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Send request to FastAPI backend
    response = requests.post(API_URL, json={"query": query})
    
    if response.status_code == 200:
        bot_reply = response.json()["response"]
    else:
        bot_reply = "❌ Error: Could not retrieve response."
    
    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Add bot message to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
