import pandas as pd
from langchain.embeddings import init_embeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

CHUNK_PARQUET = "data/sunbeam_chunks.parquet"
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "sunbeam_knowledge"

def embed_and_store():
    df = pd.read_parquet(CHUNK_PARQUET)

    embed_model = init_embeddings(
        model="text-embedding-nomic-embed-text-v1.5-embedding",
        provider="openai",
        base_url="http://127.0.0.1:1234/v1",
        api_key="none",
        check_embedding_ctx_length=False
    )

    docs = []
    ids = []

    for _, row in df.iterrows():
        docs.append(
            Document(
                page_content=row["content"],
                metadata={
                    "chunk_id": row["chunk_id"],
                    "parent_id": row["parent_id"],
                    "source": row["source"],
                    "scraper": row["scraper"]
                }
            )
        )
        ids.append(row["chunk_id"])

    vectordb = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embed_model,
        persist_directory=CHROMA_DIR
    )

    vectordb.add_documents(documents=docs, ids=ids)

    print("✅ Embeddings stored in ChromaDB")
    print(f"Collection : {COLLECTION_NAME}")
    print(f"Chunks     : {len(docs)}")

if __name__ == "__main__":
    embed_and_store()
