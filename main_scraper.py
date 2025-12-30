import pandas as pd
from datetime import datetime
import os

def save_to_parquet(documents, output_dir='data'):
    """Save scraped documents to Parquet file"""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    df = pd.DataFrame({
        'id': [f'doc_{i}' for i in range(len(documents))],
        'content': documents,
        'scraped_at': [datetime.now().isoformat()] * len(documents)
    })
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f'sunbeam_data_{timestamp}.parquet')
    
    df.to_parquet(filename, index=False)
    
    print(f"\n✓ Saved {len(documents)} documents to {filename}")
    return filename

def run_all_scrapers():
    all_documents = []

    print("\n========== RUNNING SUNBEAM SITEMAP SCRAPER ==========\n")
    from Scrape.sunbeam_scraper import run_sunbeam_scraper
    sitemap_docs = run_sunbeam_scraper()
    if sitemap_docs:
        all_documents.extend(sitemap_docs)

    print("\n========== RUNNING MODULAR COURSES SCRAPER ==========\n")
    from Scrape.sunbeam_modular_courses import run_modular_courses_scraper
    modular_docs = run_modular_courses_scraper()
    if modular_docs:
        all_documents.extend(modular_docs)

    print("\n========== RUNNING INTERNSHIP SCRAPER ==========\n")
    from Scrape.sunbeam_internship import run_internship_scraper
    internship_docs = run_internship_scraper()
    if internship_docs:
        all_documents.extend(internship_docs)

    return all_documents


if __name__ == "__main__":
    result = run_all_scrapers()

    if result:
        print("\n" + "=" * 100)
        print(f"TOTAL DOCUMENTS COLLECTED: {len(result)}")
        print("=" * 100)

        for idx, item in enumerate(result[:5], 1):
            print(f"\n[Preview {idx}]")
            print(item[:800])
            print("-" * 100)
        
        saved_file = save_to_parquet(result)
        print(f"\n✓ Data saved successfully!")