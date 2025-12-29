import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "user_chat_in" not in st.session_state:
    st.session_state.user_chat_in= ""

def initial_containers():
    with st.container(border=False,height="content",width="content",):
        with st.container(border=True,width="content"):
            with st.chat_message("ai"):
                st.write("Want to chat about sunbeam? I'm an Ai chatbot here to help you find your way")

        with st.container(border=True,height="content",width="content"):
                st.write("Ask me or select an option below 👇")

        col1,col2=st.columns(2)

        with col1 :
            if st.button("📖 Know about sunbeam",width="stretch"):
                st.session_state.user_chat_in="Know about sunbeam"
                    
        with col2 :
            if st.button("🔎 Know about courses",width="stretch"):
                st.session_state.user_chat_in="Know about courses"

        with col1 :
            if st.button("📈 know Placement stats",width="stretch"):
                st.session_state.user_chat_in="know Placement stats"
            
        with col2 :
            if st.button("💡 Internship options",width="stretch"):
                st.session_state.user_chat_in="Internship options"

def initial_sidebar():
    with st.sidebar:
        st.title("Sections",width="stretch",text_alignment="center")

        st.divider()

        if st.button("Chatbot",width="stretch"):
            pass

        if st.button("Sources",width="stretch"):
            pass

        if st.button("Analytics",width="stretch"):
            pass


st.title("🤖 SunBot")

initial_containers()
initial_sidebar()

user_input=st.chat_input("Ask me anything",key="user_chat_in")

if user_input:
    st.session_state.messages.append({
        "role" : "user",
        "content" : user_input
    })
    st.session_state.user_chat_in=""
    

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

    

