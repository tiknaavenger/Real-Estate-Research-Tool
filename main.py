# ============================================================
# Real Estate Research Tool (Streamlit + RAG)
# Description:
#   A Streamlit-based application to research real estate topics
#   using Retrieval-Augmented Generation (RAG).
#   - Users can input multiple article URLs
#   - System processes them with embeddings
#   - Users can then ask questions and get AI-generated answers
# ============================================================

import streamlit as st
from rag import process_urls, generate_answer

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Real Estate Research Tool",
    page_icon="🏠",
    layout="centered"
)

# -----------------------------
# Custom Styling (Real Estate Theme)
# -----------------------------
st.markdown("""
    <style>
        /* Title Styling */
        .main-title { 
            font-size: 32px; 
            font-weight: 700; 
            text-align: center; 
            color: #2E86C1; /* Real Estate Blue */
        }
        /* Subheader Styling */
        .sub-header { 
            font-size: 15px; 
            font-weight: 600; 
            color: #27AE60; /* Green for Growth */
        }
        /* Answer Box */
        .answer-box {
            background-color: #f9f9f9;
            border-left: 6px solid #2E86C1;
            color: #2c3e50;
            padding: 18px;
            border-radius: 10px;
            font-size: 17px;
            line-height: 1.6;
        }
        /* Source Links */
        .source-link { 
            font-size: 16px; 
            color: #2980b9; 
            margin-bottom: 5px;
        }
        .source-link a { text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Main Title
# -----------------------------
st.markdown('<div class="main-title">🏠 Real Estate Research Tool</div>', unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("🔗 Enter Article URLs")
url1 = st.sidebar.text_input("🏢 URL 1")
url2 = st.sidebar.text_input("🏢 URL 2")
url3 = st.sidebar.text_input("🏢 URL 3")

st.sidebar.markdown("---")
process_url_button = st.sidebar.button("🚀 Process URLs")

# Placeholder for status messages
placeholder = st.empty()

# -----------------------------
# URL Processing with Error Handling
# -----------------------------
if process_url_button:
    urls = [url.strip() for url in (url1, url2, url3) if url.strip()]

    if not urls:
        st.sidebar.warning("⚠️ Please provide at least one valid URL.")
    else:
        try:

            # Collect statuses first so we know how many steps
            statuses = list(process_urls(urls))
            total_steps = len(statuses)

            progress = st.progress(0, text="🏗️ Initializing processing...")

            # Simulate progress updates from process_urls
            for i, status in enumerate(process_urls(urls)):
                # Ensure value is between 0.0 and 1.0
                progress.progress(min((i + 1) / total_steps, 1.0), text=f"🔄 {status}")

            progress.empty()
            st.session_state["urls_processed"] = True
            st.success("✅ URLs processed successfully.")
        except Exception as e:
            st.error(f"❌ Error while processing URLs: {str(e)}")
            st.session_state["urls_processed"] = False

# -----------------------------
# Question Input
# -----------------------------
st.markdown("### 💬 Ask a Question")
query = st.text_input("Type your question here...")

# -----------------------------
# Answer Generation
# -----------------------------
if query:
    if not st.session_state.get("urls_processed"):
        st.error("⚠️ You must process URLs before asking a question.")
    else:
        try:
            with st.spinner("🧠 Generating answer..."):
                answer, sources = generate_answer(query)

            # Display Answer
            st.markdown("### 📢 Answer")
            st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

            # Display Sources
            if sources:
                st.markdown("### 📑 Sources")
                for source in sources.split("\n"):
                    if source.strip():
                        st.markdown(
                            f'<div class="source-link">🔗 <a href="{source}" target="_blank">{source}</a></div>',
                            unsafe_allow_html=True
                        )
        except RuntimeError:
            st.error("⚠️ You must process URLs first.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
