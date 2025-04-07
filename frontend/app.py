# frontend/app.py
import streamlit as st
import requests

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"  # change this if deploying to cloud

st.set_page_config(page_title="Financial Chatbot", layout="centered")
st.title("💼 Financial Intelligence Chatbot")

# File Upload Section
st.header("📂 Upload Files")
uploaded_files = st.file_uploader(
    "Upload multiple files (PDF, Excel, Word, CSV, etc.)",
    type=["pdf", "docx", "doc", "csv", "xlsx", "xls", "txt"],
    accept_multiple_files=True
)

if st.button("Upload Files") and uploaded_files:
    for file in uploaded_files:
        with st.spinner(f"Uploading {file.name}..."):
            response = requests.post(
                f"{BACKEND_URL}/file/upload/",  # your API route
                files={"file": (file.name, file, file.type)}
            )
            if response.status_code == 200:
                st.success(f"{file.name} uploaded successfully!")
            else:
                st.error(f"Failed to upload {file.name}")

# Chat Section
st.header("🗣️ Ask Your Questions")
query = st.text_input("Enter your query")

if st.button("Ask") and query:
    with st.spinner("Fetching answer..."):
        response = requests.post(
            f"{BACKEND_URL}/chat/ask/", json={"query": query}
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "No response")
            st.success(answer)
        else:
            st.error("Failed to get a response from the chatbot")
