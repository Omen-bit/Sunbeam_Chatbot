from langchain_chroma import Chroma
from langchain.chat_models import init_chat_model
from langchain_community.embeddings import HuggingFaceEmbeddings
from collections import defaultdict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =========================
# CONFIG
# =========================
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "sunbeam_knowledge"

# Local embeddings (NO API calls)
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"

# Groq LLM
LLM_MODEL = "openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# EMBEDDINGS (LOCAL)
# =========================
_embeddings_model = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={"trust_remote_code": True}
)

# =========================
# VECTOR STORE
# =========================
_vectordb = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=_embeddings_model,
    persist_directory=CHROMA_DIR
)

# =========================
# LLM (GROQ)
# =========================
_llm = init_chat_model(
    model=LLM_MODEL,
    model_provider="openai",
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
    temperature=0.2
)

# =========================
# QA FUNCTION
# =========================
def ask_question(query: str) -> str:
    docs = _vectordb.similarity_search(query, k=12)

    grouped = defaultdict(list)

    for d in docs:
        content = d.page_content.strip()
        if len(content) < 40:
            continue

        course = d.metadata.get("course", "Unknown Course")
        section = d.metadata.get("section", "General")
        grouped[(course, section)].append(content)

    if not grouped:
        return "Sorry, I could not find relevant information for your question."

    context_blocks = []

    for (course, section), texts in grouped.items():
        block = f"{course}\n{section}\n" + "\n".join(texts)
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""
You are an expert course advisor for Sunbeam Institute.

Rules:
- Use ONLY the information provided in the context
- Do NOT add external knowledge
- Do NOT hallucinate
- Answer clearly and professionally

Context:
{context}

Question:
{query}

Answer:
"""

    response = _llm.invoke(prompt)
    return response.content
