import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
import uuid
import os

INPUT_PARQUET = "data/sunbeam_raw_20251231_011836.parquet"
OUTPUT_PARQUET = "data/sunbeam_chunks.parquet"

MIN_CHARS = 120          
MAX_SINGLE_CHUNK = 800   

def chunk_parquet():
    df = pd.read_parquet(INPUT_PARQUET)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", " ", ""]
    )

    chunk_rows = []

    for _, row in df.iterrows():
        text = str(row.get("content", "")).strip()
        if not text:
            continue

        if len(text) <= MAX_SINGLE_CHUNK:
            chunks = [text]
        else:
            chunks = splitter.split_text(text)

        for idx, chunk in enumerate(chunks):
            chunk = chunk.strip()
            if not chunk:
                continue

            if len(chunk) < MIN_CHARS:
                prefix_lines = []
                if "course" in row and row["course"]:
                    prefix_lines.append(row["course"])

                if "section" in row and row["section"]:
                    prefix_lines.append(row["section"])

                if prefix_lines:
                    chunk = "\n".join(prefix_lines) + "\n" + chunk

            if len(chunk) < MIN_CHARS:
                continue

            chunk_rows.append({
                "chunk_id": str(uuid.uuid4()),
                "parent_id": row.get("id", ""),
                "content": chunk,
                "source": row.get("source", ""),
                "scraper": row.get("scraper", ""),
                "scraped_at": row.get("scraped_at", ""),
                "chunk_index": idx,
                "created_at": datetime.now().isoformat()
            })

    chunk_df = pd.DataFrame(chunk_rows)
    chunk_df.to_parquet(OUTPUT_PARQUET, index=False)

    print("✅ Chunking complete")
    print(f"Original docs : {len(df)}")
    print(f"Total chunks  : {len(chunk_df)}")
    print(f"Saved to      : {OUTPUT_PARQUET}")


if __name__ == "__main__":
    chunk_parquet()
