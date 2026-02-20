import sys
import time
from uuid import uuid4
from pathlib import Path

# sqlite hack if using pysqlite3 package
try:
    import pysqlite3  # type: ignore
    sys.modules["sqlite3"] = sys.modules["pysqlite3"]
except Exception:
    pass

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

import trafilatura

# ---------------------------
# Config / Constants
# ---------------------------
CHUNK_SIZE = 300         # reduced to keep chunks short and within token limits
CHUNK_OVERLAP = 50       # small overlap to preserve context across chunks
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources" / "vectorstore"
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
COLLECTION_NAME = "real_estate"

# Keep your realistic User-Agent
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

# Globals
llm = None
vector_store = None


# ---------------------------
# Initialization
# ---------------------------
def initialize_components():
    global llm, vector_store
    if llm is None:
        # Lower temperature for factual answers
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2, max_tokens=600)

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


def custom_scraper(url, timeout=15):
    """
    Production-grade scraper using trafilatura.
    Works locally and on Streamlit Cloud.
    No Selenium required.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            raise ValueError("Failed to download page")

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=False
        )

        if not text or len(text) < 500:
            raise ValueError("Extracted article text too small")

        return Document(page_content=text, metadata={"source": url})

    except Exception as e:
        raise RuntimeError(f"Failed to scrape {url}: {e}")


# ---------------------------
# Processing & RAG helpers
# ---------------------------
def process_urls(urls, reset=True):
    """
    Generator that yields status strings during processing (used by Streamlit UI).
    It scrapes each URL, prints a short preview, splits text into chunks, and adds to a Chroma vectorstore.
    """
    yield "Initializing Components"
    initialize_components()

    if reset:
        yield "Resetting vector store...✅"
        try:
            vector_store.reset_collection()
        except Exception as e:
            # if reset fails, continue but log
            yield f"Warning: reset failed ({e})"

    yield "Loading data...✅"
    data = []
    for url in urls:
        yield f"Scraping: {url}"
        try:
            doc = custom_scraper(url)
            data.append(doc)
            # Print/return a concise preview of the scraped content so user can see what was ingested
            preview = doc.page_content[:400].replace("\n", " ").strip()
            yield f"Scraped {url} ({len(doc.page_content)} chars). Preview: {preview}..."
        except Exception as e:
            yield f"❗ Error scraping {url}: {str(e)}"
            # continue to next URL

    if not data:
        yield "No valid documents were scraped. Aborting embedding."
        return

    yield "Splitting text into chunks...✅"
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    docs = text_splitter.split_documents(data)

    yield f"Add {len(docs)} chunks to vector database...✅"
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    # persist (Chroma will persist to persist_directory)
    try:
        vector_store.persist()
    except Exception:
        pass

    yield "Done adding docs to vector database...✅"


def generate_answer(query):
    """
    Run the retrieval-augmented QA chain and return (answer, sources)
    Uses only top-k retrieved chunks to avoid exceeding LLM input limits.
    """
    if vector_store is None:
        raise RuntimeError("Vector database is not initialized. Call process_urls first.")

    # Use a small k so the LLM gets only the most relevant chunks and doesn't exceed context size.
    retriever = vector_store.as_retriever(search_kwargs={"k": 8})
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=retriever)
    # Using the chain's .invoke / .run style depending on your langchain version
    try:
        result = chain.invoke({"question": query}, return_only_outputs=True)
    except Exception:
        # fallback to run if invoke is not available
        result = chain({"question": query})

    # depending on the chain return shape
    answer = result.get("answer") or result.get("output_text") or result.get("result") or ""
    sources = result.get("sources", "")
    return answer, sources


# ---------------------------
# Debug helper
# ---------------------------
def test_similarity(query, k=2):
    """
    Quick helper to inspect what the retriever returns (for debugging)
    Returns list of dicts with source and a short snippet.
    """
    if vector_store is None:
        raise RuntimeError("Vector DB not initialized")
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)
    out = []
    for d in docs:
        snippet = (d.page_content[:600] + "...") if len(d.page_content) > 600 else d.page_content
        out.append({"source": d.metadata.get("source"), "snippet": snippet})
    return out


# ---------------------------
# For manual run
# ---------------------------
if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html",
        "https://www.cnbctv18.com/real-estate/gurugram-rents-slip-in-october-december-2025-quarter-despite-rising-tenant-demand-ws-l-19853053.htm",
        "https://www.cnbctv18.com/real-estate/exclusive-why-indias-residential-housing-sales-are-slowing-despite-rising-values-ws-l-19853013.htm"
    ]

    for status in process_urls(urls, reset=True):
        pass
    # print("Done processing. Now test retrieval:")
    # print(test_similarity("What happened to Gurugram rents in Oct-Dec 2025?", k=2))

    # answer, sources = generate_answer("Tell me what was the 30 year fixed mortgage rate along with the date?")
    # answer, sources = generate_answer("What was the rental demand growth rate in Gurugram?")
    # print(f"Answer: {answer}")
    # print(f"Sources: {sources}")

    questions = [
        "What happened to Gurugram rents in Oct-Dec 2025?",
        "What was the rental demand growth rate in Gurugram?",
        "Why did Gurugram rents decline despite rising demand?",
        "How did supply change during the October–December 2025 quarter?",
        "What percentage of rental demand was in the ₹10,000–20,000 bracket?",
        "Why are India's residential housing sales slowing?"
    ]

    for i, q in enumerate(questions, 1):
        print("\n" + "=" * 60)
        print(f"Question {i}: {q}")
        print("=" * 60)

        answer, sources = generate_answer(q)

        print("Answer:", answer)
        print("Sources:", sources)