<h2 align="center">🏡 Real Estate Research Tool – AI-Powered Insight Engine</h2>

<p align="center"><b>An intelligent research assistant that makes sense of real estate news by combining web scraping, semantic search, and large language models.</b></p>

<p align="center"><b>This project transforms unstructured property-related articles into an interactive knowledge base where you can ask natural questions and receive clear, referenced answers.</b></p>

<p align="center">
  <a href="https://www.langchain.com/"><img alt="LangChain" src="https://img.shields.io/badge/🔗%20LangChain-0.3.27-1d4ed8?logo=chainlink&logoColor=white"></a>
  <a href="https://www.trychroma.com/"><img alt="Chroma" src="https://img.shields.io/badge/🟣%20LangChain--Chroma-0.2.5-9333ea?logo=databricks&logoColor=white"></a>
  <a href="https://python.langchain.com/docs/integrations/community"><img alt="LangChain Community" src="https://img.shields.io/badge/🌐%20LangChain--Community-0.3.29-2563eb?logo=github&logoColor=white"></a>
  <a href="https://python.langchain.com/docs/modules/core_concepts"><img alt="LangChain Core" src="https://img.shields.io/badge/⚙️%20LangChain--Core-0.3.75-0f766e?logo=apache&logoColor=white"></a>
  <a href="https://groq.com/"><img alt="LangChain Groq" src="https://img.shields.io/badge/⚡%20LangChain--Groq-0.3.7-facc15?logo=lightning&logoColor=black"></a>
  <a href="https://huggingface.co/"><img alt="LangChain HuggingFace" src="https://img.shields.io/badge/🤗%20LangChain--HuggingFace-0.3.1-ef4444?logo=huggingface&logoColor=white"></a>
  <a href="https://pypi.org/project/python-dotenv/"><img alt="python-dotenv" src="https://img.shields.io/badge/🌱%20python--dotenv-1.1.0-22c55e?logo=.env&logoColor=white"></a>
  <a href="https://requests.readthedocs.io/"><img alt="Requests" src="https://img.shields.io/badge/🌐%20Requests-2.32.5-2563eb?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/%20Streamlit-1.45.0-ff4b4b?logo=streamlit&logoColor=white"></a>
  <a href="https://www.sbert.net/"><img alt="Sentence Transformers" src="https://img.shields.io/badge/📝%20Sentence--Transformers-5.0.0-8b5cf6?logo=transformers&logoColor=white"></a>
</p>


---

## 🚀 What This Project Does

- **Scrape** 📑 – Fetches content from real estate news/article URLs.

- **Embed** 🔗 – Generates semantic vector embeddings for context-aware search.

- **Store** 🗄️ – Saves embeddings in a vector database for fast retrieval.

- **Query** 💬 – Lets users ask natural questions and receive grounded, source-backed responses powered by modern LLMs.
---

## ✔️ Key Features
1. Multi-URL input for bulk article analysis.
2. Contextual embeddings for smarter search results
3. Lightning-fast vector database queries (ChromaDB)
4. Answers with citations to original sources
5. Simple and intuitive Streamlit interface

---
## 🚀 Launch App
[https://real-estate-research-tool.streamlit.app/](https://real-estate-research-tool.streamlit.app/)

![app](Project%20Screenshot%201.JPG)


### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/tiknaavenger/Real_Estate_Research_Tool.git
   cd Real_Estate_Research_Tool
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**

   ```bash
   streamlit run app.py
   ```

---

## ⚙️ How It Works
1. **Provide URLs →** Input one or multiple article links.
2. **Automatic Processing →** Text is scraped, cleaned, and embedded.
3. **Storage →** Embeddings are indexed inside ChromaDB.
4. **Ask Anything →** Users query in plain English.
5. **AI Response →** System retrieves relevant chunks and responds with clear, referenced answers.

---

## Contributing

To Contribute, please submit issues or pull requests for enhancements or fixes.

---

## License

Licensed under the Apache 2.0 License.

---
