# 🤖 Sunbeam Chatbot

An AI-powered chatbot that intelligently answers questions about Sunbeam Institute by extracting and processing information from the institute's website. It uses web scraping, NLP, and Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses.

![Streamlit](https://img.shields.io/badge/Streamlit-1.52-red?style=flat&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.39-green?style=flat&logo=selenium)
![LangChain](https://img.shields.io/badge/LangChain-1.2-orange?style=flat)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.4-purple?style=flat)
![Pandas](https://img.shields.io/badge/Pandas-2.3-black?style=flat&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Data Pipeline](#data-pipeline)
- [Contributing](#contributing)

## ✨ Features

- **Intelligent Web Scraping**: Automatically extracts content from Sunbeam Institute website
- **Multi-Source Data Collection**: Gathers information from:
  - General pages (about, placements, branches)
  - Modular courses
  - Internship programs
- **RAG-Powered Q&A**: Uses Retrieval-Augmented Generation for accurate, context-based answers
- **Interactive UI**: Streamlit-based chat interface with quick-access buttons
- **Data Persistence**: Stores scraped data in Parquet format for efficient processing
- **Deduplication**: Removes duplicate content automatically

## 🛠️ Tech Stack

- **Web Scraping**: Selenium, BeautifulSoup, Requests
- **Data Processing**: Pandas, PyArrow
- **LLM & Embeddings**: LangChain, Google Generative AI, Sentence Transformers
- **Vector Database**: Chromadb
- **Frontend**: Streamlit
- **Backend**: Python 3.x
- **Data Format**: Parquet

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Sunbeam_Chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required directories**
   ```bash
   mkdir -p data public
   ```

## 📖 Usage

### Run the Chatbot UI

```bash
streamlit run main.py
```

The chatbot will launch at `http://localhost:8501`

### Scrape Data

```bash
python main_scraper.py
```

This will:
- Scrape all three sources (general pages, courses, internships)
- Deduplicate content
- Save to `data/sunbeam_YYYYMMDD_HHMMSS.parquet`

### Inspect Scraped Data

```bash
python test.py
```

Shows comprehensive statistics and content preview of the latest Parquet file.

## 🏗️ Architecture

### Data Pipeline

```
Website → Selenium/BeautifulSoup → Clean & Extract
    ↓
Deduplicate (SHA-256 hashing) → Pandas DataFrame
    ↓
Save to Parquet → Vector Embeddings (Sentence Transformers)
    ↓
ChromaDB Vector Store → RAG Pipeline
    ↓
LLM (Google Generative AI) → Response → User
```

### Scraper Modules

1. **sunbeam_scraper.py**: Extracts from static pages
   - About, Placements, Branches
   - Uses Selenium + BeautifulSoup
   - Filters noise (headers, footers, social links)

2. **sunbeam_modular_courses.py**: Extracts course information
   - Navigates course cards dynamically
   - Waits for elements to load
   - Extracts detailed course content

3. **sunbeam_internship.py**: Extracts internship details
   - HTTP requests (lighter weight)
   - Parses accordion sections
   - Organizes by section type

### Data Schema

```python
{
    "doc_id": "SHA-256 hash of content",
    "content": "Extracted text",
    "source": "site_pages | modular_course | internship",
    "section": "Page/course/category name",
    "url": "Source URL",
    "scraped_at": "UTC timestamp"
}
```

## 🔧 Configuration

Update these in respective files:

- **Scraper URLs**: Edit `SITEMAP` in `Scrape/sunbeam_scraper.py`
- **Parquet location**: Change `PARQUET_PATH` in `test.py`
- **UI theme**: Modify Streamlit config in `.streamlit/config.toml`

## 📊 Data Quality

- **Deduplication**: SHA-256 hashing of content
- **Noise filtering**: Excludes contact forms, ads, social links
- **Content validation**: Minimum length requirements per text type
- **Timestamp tracking**: All records timestamped

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## ⚠️ Notes

- **Dynamic content**: Selenium with explicit waits for JavaScript-rendered content
- **Rate limiting**: Scrapers include delays to respect server load
- **Error handling**: Graceful fallback for failed scrapes
- **Headless mode**: Chrome runs headless for efficiency

## 📝 License

[Add your license here]

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Last Updated**: December 2024
