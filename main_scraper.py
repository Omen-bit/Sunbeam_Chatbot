import pandas as pd
from datetime import datetime
import os
import uuid

def run_all_scrapers():
    all_documents = []

    from Scrape.sunbeam_scraper import run_sunbeam_scraper
    from Scrape.sunbeam_modular_courses import run_modular_courses_scraper
    from Scrape.sunbeam_internship import run_internship_scraper

    all_documents.extend(run_sunbeam_scraper())
    all_documents.extend(run_modular_courses_scraper())
    all_documents.extend(run_internship_scraper())

    return all_documents


def save_to_parquet(documents, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    rows = []
    now = datetime.now().isoformat()

    for doc in documents:
        rows.append({
            "id": str(uuid.uuid4()),
            "url": doc["url"],
            "content": doc["content"],
            "char_count": doc["char_count"],
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
    print(f"✅ Saved {len(df)} rows → {filename}")

    return filename


if __name__ == "__main__":
    docs = run_all_scrapers()
    save_to_parquet(docs)
