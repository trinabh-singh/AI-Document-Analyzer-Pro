import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📚 Production RAG System")

st.header("Upload PDFs")

uploaded_files = st.file_uploader(
    "Choose PDFs",
    type="pdf",
    accept_multiple_files=True
)

if st.button("Upload"):

    if uploaded_files:

        files = []

        for file in uploaded_files:
            files.append(
                (
                    "files",
                    (file.name, file, "application/pdf")
                )
            )

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        data = response.json()

        st.success(data["message"])

        st.write("### Uploaded Files")

        for file in data["files"]:
            st.write(f"📄 {file}")

        st.info(f"Chunks Created: {data['chunks_created']}")

st.divider()

question = st.text_input("Ask a question")

if st.button("Ask"):

    response = requests.post(
        f"{API_URL}/query",
        json={"question": question}
    )

    if response.status_code == 200:

        data = response.json()

        st.subheader("Answer")
        st.write(data["answer"])

    else:

        st.error(f"Backend Error ({response.status_code})")
        st.code(response.text)