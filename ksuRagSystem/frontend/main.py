import streamlit as st
from streamlit_chat import message
import time
from ksuRagSystem.backend.core import run_llm

# Render the header immediately
st.header("دليل الطالب")

# Initialize chat history in session state if not already done
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

prompt = st.text_input("الامر:", placeholder="...ادخل الامر", key="input_text")

if prompt:
    with st.spinner("...جاري الرد"):
        # Pass the loaded model from session state to your run_llm function
        generated_response = run_llm(
            query=prompt,
            chat_history=st.session_state["chat_history"],
        )

        formatted_response = generated_response['result']

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

        # Clear the input text field after submission
        st.session_state["input_text"] = ""

# Display the chat history
if st.session_state["chat_answers_history"]:
    for user_query, generated_response in zip(
        st.session_state["user_prompt_history"],
        st.session_state["chat_answers_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)