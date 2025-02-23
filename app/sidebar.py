import streamlit as st
from api_utils import upload_doc, list_documents


def sidebar():

    # Upload docs
    st.sidebar.title('Upload Documents')
    uploaded_file = st.sidebar.file_uploader("Upload your documents", type=['pdf'])
    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner('Uploading...'):
                upload_response = upload_doc(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File {uploaded_file.name} has been successfully uploaded and indexed. File ID: {upload_response['file_id']}")
                    st.session_state.documents = list_documents()