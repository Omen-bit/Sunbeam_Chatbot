# 🤖 Sunbeam Chatbot

An AI-powered chatbot that intelligently answers questions about Sunbeam Institute by extracting and processing information from the institute's website. It uses web scraping, NLP, and Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses.

![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red?style=flat&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.39-green?style=flat&logo=selenium)
![LangChain](https://img.shields.io/badge/LangChain-1.2-orange?style=flat)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.4-purple?style=flat)

## ✨ Features

- **Intelligent Web Scraping**: Automatically extracts content from Sunbeam Institute website
- **Multi-Source Data Collection**: General pages, modular courses, and internship programs
- **RAG-Powered Q&A**: Retrieval-Augmented Generation for accurate, context-based answers
- **Interactive UI**: Streamlit-based chat interface with quick-access buttons
- **Data Persistence**: Stores scraped data in Parquet format
- **Deduplication**: Removes duplicate content automatically

## 🛠️ Tech Stack

- **Web Scraping**: Selenium, BeautifulSoup, Requests
- **Data Processing**: Pandas, PyArrow
- **LLM & Embeddings**: LangChain, Google Generative AI, Sentence Transformers
- **Vector Database**: Chromadb
- **Frontend**: Streamlit

## 🚀 Quick Start

### Installation

```bash
git clone <repo-url>
cd Sunbeam_Chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
mkdir -p data public
```

### Usage

**Run the chatbot:**
```bash
streamlit run main.py
```

**Scrape data:**
```bash
python main_scraper.py
```

**Inspect data:**
```bash
python test.py
```

## 🏗️ How It Works

1. **Web Scrapers** extract content from Sunbeam website (courses, internships, general info)
2. **Data Processing** deduplicates and cleans content
3. **Vector Embeddings** convert text to embeddings using Sentence Transformers
4. **ChromaDB** stores embeddings for semantic search
5. **RAG Pipeline** retrieves relevant context and generates answers via LLM
6. **Streamlit UI** provides interactive chat interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

---

**Last Updated**: December 2024
