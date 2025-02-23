import streamlit as st
from api_utils import get_response

def chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            response = get_response(prompt, st.session_state.session_id)
            print(response)
            if response:
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['response']})
                
                with st.chat_message("assistant"):
                    st.markdown(response['response'])
                    
                    with st.expander("Details"):
                        st.subheader("Generated Answer")
                        st.code(response['response'])
                        st.subheader("Session ID")
                        st.code(response['session_id'])
            else:
                st.error("Failed to get a response from the API. Please try again.")