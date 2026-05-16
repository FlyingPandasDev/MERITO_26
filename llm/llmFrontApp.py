import streamlit as st
from datetime import datetime
from src.chat.chatOrchestrator import handle_user_message, start_user_session

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.log.append(f"[{ts}] {msg}")

# ---------- init state (runs every rerun, but only sets defaults once)
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "🐼", "content": "Hello 👋"}]

if "pending_msg" not in st.session_state:
    st.session_state.pending_msg = None
if "log" not in st.session_state:
    st.session_state.log = []

# ---------- sidebar: login + log
with st.sidebar:
    #st.session_state.is_logged_in = True
    if st.session_state.is_logged_in == False:
        st.subheader("Login")
        user_id_input = st.text_input("User ID", value="Tester")
        st.session_state.user_id = user_id_input
        #user_chosen_model = st.selectbox("Model", options =["local", "Bielik"])
        st.session_state.model = "ai"

        if st.button("Login"):
            allowed, model_status = start_user_session(user_id_input)
            if allowed:
                st.session_state.is_logged_in = True
                log(f"Login OK")

                if model_status:
                    log("Handshake successfull, chat was created")
                else:
                    log("Handshake error")
                    st.error("Handshake error")
                st.rerun()
            else:
                st.session_state.is_logged_in = False
                st.session_state.user_id = None
                st.error("Access denied")
    else:
        user_id_input = st.session_state.user_id
        st.subheader("Zalogowany jako:")
        st.write(user_id_input)
    st.divider()
    st.subheader("Backend log")
    if st.button("Clear log"):
        st.session_state.log = []
    st.write("\n".join(st.session_state.log[-200:]) or "(empty)")

# ---------- main: gate chat on session flag (NOT on the login button)
if not st.session_state.is_logged_in:
    st.info("Enter User ID and click Login to continue.")
    st.stop()
else:
    st.toast("🐼 Logged in Successfully")
    st.title("Flying Pandas 🐼")




# ---------- render chat
for m in st.session_state.messages:
    
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ---------- phase 2: process pending message (LLM call)
if st.session_state.pending_msg:
    msg = st.session_state.pending_msg
    st.session_state.pending_msg = None

    log("Calling backend handler")
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            logged_in = st.session_state.is_logged_in
            user_id = st.session_state.user_id
            user_chosen_model = st.session_state.model


            header = {
                "logged_in" : logged_in,
                "user_chosen_model" : user_chosen_model
            }
            reply, user_backend_object, microservice_llm_reply, hasFile = handle_user_message(msg, header, logger=log)
    log("Backend handler finished")
    #hasFile = True

    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
        log("Appended assistant reply")
    if microservice_llm_reply:
        st.session_state.messages.append({"role": "assistant", "content": microservice_llm_reply})
        log("Appended assistant reply")
    if hasFile == True:
        st.session_state.messages.append({"role": "assistant", "content": user_backend_object})
        log("Appended assistant reply with object")

    st.rerun()


# ---------- phase 1: accept input (show user msg immediately)
user_msg = st.chat_input("Say something")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    log("User message received")
    st.session_state.pending_msg = user_msg
    st.rerun()