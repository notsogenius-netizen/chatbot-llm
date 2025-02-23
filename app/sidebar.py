import streamlit as st
from api_utils import upload_doc, list_documents, delete_document


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

    # List docs
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")
        
        # Delete Document
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents()  # Refresh the list after deletion
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")