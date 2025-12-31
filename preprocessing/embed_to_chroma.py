def run_embed_and_store():
    import pandas as pd
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    from langchain_huggingface import HuggingFaceEmbeddings

    CHUNK_PARQUET = "..\\data\\sunbeam_chunks.parquet"
    CHROMA_DIR = "..\\chroma_db"
    COLLECTION_NAME = "sunbeam_knowledge"

    def embed_and_store():
        df = pd.read_parquet(CHUNK_PARQUET)

        embedding_model = HuggingFaceEmbeddings(
            model_name="nomic-ai/nomic-embed-text-v1.5",
            model_kwargs={
                "device": "cpu",
                "trust_remote_code": True
            },
            encode_kwargs={"normalize_embeddings": True}
        )

        docs = []
        ids = []

        for _, row in df.iterrows():
            docs.append(
                Document(
                    page_content=row["content"],
                    metadata={
                        "chunk_id": row["chunk_id"],
                        "parent_id": row.get("parent_id", ""),
                        "source": row.get("source", ""),
                        "scraper": row.get("scraper", "")
                    }
                )
            )
            ids.append(row["chunk_id"])

        vectordb = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=CHROMA_DIR
        )

        vectordb.add_documents(documents=docs, ids=ids)

        print("Embeddings stored")
        print(len(docs))

    embed_and_store()


if __name__ == "__main__":
    run_embed_and_store()
