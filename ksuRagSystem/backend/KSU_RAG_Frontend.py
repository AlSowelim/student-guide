from typing import Set

from core import run_llm
import streamlit as st
from streamlit_chat import message
from arabic_support import support_arabic_text

# Support Arabic text alignment in all components
support_arabic_text(all = True)

st.title(":robot_face: _مساعد الطالب :blue[الذكي]_")
#st.markdown("<h1 style='text-align: center; color: blue;'> مساعد الطالب الذكي</h1>", unsafe_allow_html=True)
st.write("") #New line

# Add KSU logo
logo_url = "/Users/yazeedalfaify/PycharmProjects/ksuRagSystem/frontend/KSUlogo.jpg"
st.image(logo_url, width=100)

# A brief app description
st.write("") # New line
st.header("عن البرنامج")
st.write("**مرحبًا! أنا مساعدك الذكي المصمم خصيصًا لتزويدك بمعلومات حول جامعة الملك سعود. سواء كنت تبحث عن تفاصيل حول التخصصات الأكاديمية، أو الفعاليات الجامعية، أو الخدمات المتاحة، أنا هنا للمساعدة. لا تتردد في طرح أي سؤال يتعلق بالجامعة وسأكون سعيدًا بتقديم الإجابة**")

# Check streamlit docs for more info

prompt = st.text_input("الامر:", placeholder="أسالني عن اي شيء يخص الجامعة!")

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


# def create_sources_string(source_urls: Set[str]) -> str:
#     if not source_urls:
#         return ""
#     sources_list = list(source_urls)
#     sources_list.sort()
#     sources_string = "sources:\n"
#     for i, source in enumerate(sources_list):
#         sources_string += f"{i+1}. {source}\n"
#     return sources_string


if prompt:
    with st.spinner("...جاري الرد"):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        formatted_response = (
            f"{generated_response['result']} "
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))


if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)