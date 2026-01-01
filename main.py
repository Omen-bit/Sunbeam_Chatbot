import streamlit as st
import pandas as pd
import glob
import os
from retrieval.qa_engine import ask_question

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_text" not in st.session_state:
    st.session_state.chat_text = ""

if "prefill_text" not in st.session_state:
    st.session_state.prefill_text = ""

if "active_page" not in st.session_state:
    st.session_state.active_page = "chat"

def initial_containers():
    with st.container():
        with st.container(border=True):
            with st.chat_message("ai"):
                st.write("Want to chat about Sunbeam? I'm an AI chatbot here to help you find your way.")

        with st.container(border=True):
            st.write("Ask me or select an option below 👇")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📖 Know about Sunbeam", use_container_width=True):
                st.session_state.prefill_text = "Know about Sunbeam"

        with col2:
            if st.button("🔎 Know about courses", use_container_width=True):
                st.session_state.prefill_text = "Know about courses"

        with col1:
            if st.button("📈 Know placement stats", use_container_width=True):
                st.session_state.prefill_text = "Know placement stats"

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
            if st.button("Chatbot", use_container_width=True):
                st.session_state.active_page = "chat"

        with col1:
            st.image("public/source.png", width=40)
        with col2:
            if st.button("Source", use_container_width=True):
                st.session_state.active_page = "source"

def source_page():
    st.header("📚 Scraped Sources")

    files = glob.glob("data/*.parquet")
    files = [f for f in files if "sunbeam_raw" in f]

    if not files:
        st.warning("No scraped data found.")
        return

    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    summary = df.groupby("url", as_index=False)["char_count"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total URLs Scraped", summary["url"].nunique())
    col2.metric("Total Characters Scraped", int(summary["char_count"].sum()))

    for _, row in summary.iterrows():
        with st.expander(row["url"]):
            st.write(f"Characters scraped: {row['char_count']}")

col1, col2 = st.columns([0.10, 0.90], gap="small")

with col1:
    st.image("public/chat_icon.png", width=70)

with col2:
    st.markdown("<h1 style='margin-top:-17px;'>SunBot</h1>", unsafe_allow_html=True)

initial_sidebar()

if st.session_state.active_page == "chat":
    initial_containers()
elif st.session_state.active_page == "source":
    source_page()

if st.session_state.active_page == "chat":
    if st.session_state.prefill_text:
        st.session_state.chat_text = st.session_state.prefill_text
        st.session_state.prefill_text = ""

    user_input = st.chat_input("Ask me anything", key="chat_text")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        result = ask_question(user_input)

        if isinstance(result, dict):
            answer_text = result.get("answer", "")
            sources = result.get("sources", [])
        else:
            answer_text = result
            sources = []

        final_answer = answer_text
        if sources:
            final_answer += "\n\nSources:\n"
            for src in sources:
                final_answer += f"- {src}\n"

        st.session_state.messages.append(
            {"role": "assistant", "content": final_answer}
        )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
