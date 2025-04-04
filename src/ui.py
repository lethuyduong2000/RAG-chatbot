import streamlit as st
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

st.title("🛍️ E-commerce Chatbot")

history_chat = [
    "ChatBot: Chào bạn! Mình là trợ lý ảo DTN Assistant. Mình có thể tư vấn gì cho bạn!"
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
if "rerank" not in st.session_state:
    st.session_state.rerank = False
if "clicked" not in st.session_state:
    st.session_state.clicked = False


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
# query = st.chat_input("Ask me about products...")
query = st.chat_input("Ask me")


def vote(action):
    st.write(f"You {action}?")
    name = st.text_input("Họ và tên")
    # email = st.text_input("Email")
    # address = st.text_area("Địa chỉ giao hàng")
    if st.button("Submit"):
        st.session_state.vote = {"action": action, "name": name}
        st.rerun()


@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()
def send_confirmation_email(to_email, name):
    sender_email = "lethuyduong2000@gmail.com"
    sender_password = "rday pgdh supq kjgp"

    subject = "Xác nhận đơn hàng từ Namperfume"
    body = f"""
    Xin chào {name}
    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        print("Email error:", e)
        return False
                          

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
    # st.session_state.rerank = True
    if "rerank" in response.json():
        st.session_state.rerank = True

if st.session_state.rerank and not st.session_state.order_confirmed:
    if st.button("🛒 Mua sản phẩm này"):
        st.session_state.order_confirmed = True
        st.rerun()

if st.session_state.order_confirmed:
    with st.popover("📝 Điền thông tin đặt hàng"):
        st.markdown("### 🧾 Thông tin đặt hàng")

        with st.form("order_form"):
            name = st.text_input("Họ và tên")
            email = st.text_input("Email")
            address = st.text_area("Địa chỉ giao hàng")

            submitted = st.form_submit_button("Gửi đơn hàng")
            if submitted:
                st.success("✅ Đã gửi đơn hàng thành công!")
                st.session_state.order_confirmed = False

                success = send_confirmation_email(email, name)
                if success:
                    st.success("✅ Đã gửi đơn hàng và email xác nhận thành công!")
                else:
                    st.error("❌ Gửi email thất bại. Vui lòng thử lại.")
                st.session_state.order_confirmed = False
                st.rerun()