import pandas as pd
from datetime import datetime
import os
import uuid

def run_all_scrapers():
    all_documents = []

    print("\n========== RUNNING SUNBEAM SITEMAP SCRAPER ==========\n")
    from Scrape.sunbeam_scraper import run_sunbeam_scraper
    docs = run_sunbeam_scraper()
    if docs:
        for d in docs:
            all_documents.append({
                "content": d,
                "source": "sunbeam",
                "scraper": "sitemap"
            })

    print("\n========== RUNNING MODULAR COURSES SCRAPER ==========\n")
    from Scrape.sunbeam_modular_courses import run_modular_courses_scraper
    docs = run_modular_courses_scraper()
    if docs:
        for d in docs:
            all_documents.append({
                "content": d,
                "source": "sunbeam",
                "scraper": "modular"
            })

    print("\n========== RUNNING INTERNSHIP SCRAPER ==========\n")
    from Scrape.sunbeam_internship import run_internship_scraper
    docs = run_internship_scraper()
    if docs:
        for d in docs:
            all_documents.append({
                "content": d,
                "source": "sunbeam",
                "scraper": "internship"
            })

    return all_documents


def save_to_parquet(documents, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    now = datetime.now().isoformat()

    rows = []
    for doc in documents:
        rows.append({
            "id": str(uuid.uuid4()),
            "content": str(doc["content"]),   
            "source": doc["source"],
            "scraper": doc["scraper"],
            "scraped_at": now
        })

    df = pd.DataFrame(rows)

    filename = os.path.join(
        output_dir,
        f"sunbeam_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
    )

    df.to_parquet(filename, index=False)

    print(f"\n✅ RAW PARQUET SAVED")
    print(f"Rows: {len(df)}")
    print(f"File: {filename}")

    return filename


if __name__ == "__main__":
    documents = run_all_scrapers()

    print("\n" + "=" * 100)
    print(f"TOTAL DOCUMENTS COLLECTED: {len(documents)}")
    print("=" * 100)

    save_to_parquet(documents)
