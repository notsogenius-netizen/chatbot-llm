import streamlit as st
from sidebar import sidebar
from chat import chat

st.title('AI Chatbot')

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

sidebar()

chat()