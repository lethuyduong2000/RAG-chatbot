import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

st.title("🛍️ E-commerce Chatbot")

history_chat = [
    "ChatBot: Chào bạn! Mình là trợ lý ảo của Namperfume. Bạn muốn tìm nước hoa nào?"
]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Chào bạn! Mình là trợ lý ảo của Namperfume. Bạn muốn tìm nước hoa nào?"
    })
if "customer_preferences" not in st.session_state:
    st.session_state.customer_preferences = {}
if "order_confirmed" not in st.session_state:
    st.session_state.order_confirmed = False


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
# query = st.chat_input("Ask me about products...")
query = st.chat_input("Ask me")

if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

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
    
    if "đề xuất" in response.json():
            st.session_state.recommendations = response.json()["recommendations"]
            if st.button("🛒 Mua sản phẩm này"):
                st.session_state.order_confirmed = True
                st.rerun()

    if st.session_state.order_confirmed:
        st.subheader("📝 Điền thông tin đặt hàng")
        name = st.text_input("Họ và tên")
        email = st.text_input("Email")
        address = st.text_area("Địa chỉ giao hàng")
    