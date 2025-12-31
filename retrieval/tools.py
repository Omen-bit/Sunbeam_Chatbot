from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from collections import defaultdict
import os

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "sunbeam_knowledge"

_embeddings_model = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={"trust_remote_code": True}
)

_vectordb = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=_embeddings_model,
    persist_directory=CHROMA_DIR
)


@tool
def retrieve_sunbeam_knowledge(query: str) -> str:
    """
    Retrieve relevant course-related information from the Sunbeam knowledge base.

    Args:
        query (str): User question.

    Returns:
        str: Structured context extracted from vector database.
    """
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
        return "NO_RELEVANT_CONTEXT"

    blocks = []
    for (course, section), texts in grouped.items():
        block = f"{course}\n{section}\n" + "\n".join(texts)
        blocks.append(block)

    return "\n\n---\n\n".join(blocks)


@tool
def refine_user_query(query: str) -> str:
    """
    Refine vague or short user queries into a clearer form for better retrieval.

    Args:
        query (str): Original user query.

    Returns:
        str: Refined query.
    """
    return f"Detailed explanation of: {query}"
