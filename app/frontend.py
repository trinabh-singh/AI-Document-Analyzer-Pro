import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Production RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------- CSS --------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

h1,h2,h3{
    color:white;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:48px;
    font-weight:bold;
}

.stTextInput>div>div>input{
    border-radius:12px;
}

.metric-card{
    background:#1f2937;
    padding:18px;
    border-radius:15px;
    text-align:center;
    border:1px solid #374151;
}

.answer-box{
    background:#111827;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #3b82f6;
}

.source-card{
    background:#1f2937;
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# -------------------- Session State --------------------

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "chunks" not in st.session_state:
    st.session_state.chunks = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# -------------------- Sidebar --------------------

with st.sidebar:

    st.title("📊 Analytics")

    st.markdown("Coming Soon...")

    st.divider()

    st.metric("Documents", len(st.session_state.uploaded_files))
    st.metric("Chunks", st.session_state.chunks)

# -------------------- Header --------------------

st.title("🤖 Production RAG Assistant")

st.caption(
    "Hybrid Retrieval • BM25 • Dense Embeddings • Cross Encoder • FastAPI • Qdrant"
)

# -------------------- Metrics --------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
<div class="metric-card">
<h3>📄 Documents</h3>
<h2>{len(st.session_state.uploaded_files)}</h2>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
<div class="metric-card">
<h3>🧩 Chunks</h3>
<h2>{st.session_state.chunks}</h2>
</div>
""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
<div class="metric-card">
<h3>⚡ Retrieval</h3>
<h2>Hybrid</h2>
</div>
""",
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
<div class="metric-card">
<h3>🤖 Reranker</h3>
<h2>Enabled</h2>
</div>
""",
        unsafe_allow_html=True,
    )

st.subheader("📂 Upload PDFs")

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type="pdf",
    accept_multiple_files=True
)

if st.button("📤 Upload PDFs"):

    if uploaded_files:

        files = []

        for file in uploaded_files:

            files.append(
                (
                    "files",
                    (file.name, file, "application/pdf")
                )
            )

        with st.spinner("Uploading and indexing PDFs..."):

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

        if response.status_code == 200:

            data = response.json()

            st.success("✅ Documents indexed successfully!")

            st.session_state.uploaded_files = data["files"]
            st.session_state.chunks = data["chunks_created"]
            st.session_state.chat_history = []

        else:

            st.error(response.text)

st.divider()

# -------------------- Question --------------------

st.subheader("💬 Ask Your Documents")

question = st.text_input(
    "",
    placeholder="Ask anything about your uploaded PDFs..."
)

if st.button("🚀 Generate Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/query",
                json={
                    "question": question
                }
            )

        try:

            data = response.json()

            if "error" in data:
                st.error(data["error"])

            else:

                st.divider()

                st.session_state.chat_history.append({
                    "question": question,
                    "answer": data["answer"],
                    "sources": data.get("chunks", [])
                })

                st.markdown(
                    f"""
<div class="answer-box">

{data["answer"]}

</div>
""",
                    unsafe_allow_html=True,
                )

                # ---------------- Sources ----------------

                #if "chunks" in data:

                    #st.divider()

                    #st.subheader("📚 Sources")

                    #for chunk in data["chunks"]:

                        #meta = chunk["metadata"]

                        #with st.expander(
                            #f'📄 {meta["document_name"]} | Page {meta["page_number"]}'
                        #):

                           #st.write(chunk["chunk"])

                            #if "rerank_score" in chunk:
                                #st.caption(
                                    #f"Reranker Score : {chunk['rerank_score']:.2f}"
                                #)

        except Exception:

            st.error("Backend did not return valid JSON.")
            st.code(response.text)
for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):

        st.markdown(chat["answer"])

        if chat["sources"]:

            with st.expander("📚 Sources"):

                for chunk in chat["sources"]:

                    meta = chunk["metadata"]

                    st.write(
                        f"**{meta['document_name']}** | "
                        f"Page {meta['page_number']}"
                    )

                    st.write(chunk["chunk"])

                    if "rerank_score" in chunk:
                        st.caption(
                            f"Reranker Score: {chunk['rerank_score']:.2f}"
                        )

st.divider()

st.caption(
    "Built with ❤️ using FastAPI, Qdrant, Hybrid Retrieval, Cross Encoder and OpenRouter"
)