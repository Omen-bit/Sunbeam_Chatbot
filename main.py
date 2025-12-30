import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_text" not in st.session_state:
    st.session_state.chat_text = ""

if "prefill_text" not in st.session_state:
    st.session_state.prefill_text = ""

def initial_containers():
    with st.container():
        with st.chat_message("ai"):
            with st.container(border=True):
                st.write("Want to chat about sunbeam? I'm an Ai chatbot here to help you find your way")

        with st.container(border=True):
            st.write("Ask me or select an option below 👇")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📖 Know about sunbeam", use_container_width=True):
                st.session_state.prefill_text = "Know about sunbeam"

        with col2:
            if st.button("🔎 Know about courses", use_container_width=True):
                st.session_state.prefill_text = "Know about courses"

        with col1:
            if st.button("📈 know Placement stats", use_container_width=True):
                st.session_state.prefill_text = "know Placement stats"

        with col2:
            if st.button("💡 Internship options", use_container_width=True):
                st.session_state.prefill_text = "Internship options"

def initial_sidebar():
    with st.sidebar:
        st.title("🤖 Sunbeam Chatbot", text_alignment="center")
        st.divider()

        col1, col2 = st.columns([0.2, 0.8])

        with col1:
            st.image("public/chatbot_icon.png", width=50)
        with col2:
            st.button("Chatbot", use_container_width=True)

        with col1:
            st.image("public/analytics_icon.png", width=38)
        with col2:
            st.button("Analytics", use_container_width=True)

        with col1:
            st.image("public/source.png", width=40)
        with col2:
            st.button("Source", use_container_width=True)

st.title("🤖 SunBot")

initial_containers()
initial_sidebar()

if st.session_state.prefill_text:
    st.session_state.chat_text = st.session_state.prefill_text
    st.session_state.prefill_text = ""

user_input = st.chat_input("Ask me anything", key="chat_text")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

with st.container():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
