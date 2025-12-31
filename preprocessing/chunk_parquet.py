def run_chunk_parquet():
    import pandas as pd
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from datetime import datetime
    import uuid
    import os

    INPUT_PARQUET = "..\\data\\sunbeam_raw_20251231_151046.parquet"
    OUTPUT_PARQUET = "..\\data\\sunbeam_chunks.parquet"


    MIN_CHARS = 150
    MAX_SINGLE_CHUNK = 900

    CHUNK_SIZE = 650
    CHUNK_OVERLAP = 100

    def chunk_parquet():
        if not os.path.exists(INPUT_PARQUET):
            raise FileNotFoundError(f"Input parquet not found: {INPUT_PARQUET}")

        df = pd.read_parquet(INPUT_PARQUET)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
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

                prefix_lines = []

                if row.get("course"):
                    prefix_lines.append(f"Course: {row['course']}")

                if row.get("section"):
                    prefix_lines.append(f"Section: {row['section']}")

                if prefix_lines:
                    chunk = "\n".join(prefix_lines) + "\n\n" + chunk

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

        if not chunk_rows:
            raise ValueError("No chunks were generated. Check input data.")

        chunk_df = pd.DataFrame(chunk_rows)
        chunk_df.to_parquet(OUTPUT_PARQUET, index=False)

        print("\n✅ Chunking complete")
        print(f"Original documents : {len(df)}")
        print(f"Total chunks       : {len(chunk_df)}")
        print(f"Saved to           : {OUTPUT_PARQUET}")

    chunk_parquet()

if __name__ == "__main__":
    run_chunk_parquet()