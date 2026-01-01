def run_sunbeam_scraper():
    import time
    import re
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    def clean_text(t):
        t = re.sub(r'\s+', ' ', t)
        return t.replace('CLICK TO REGISTER', '').strip()

    def is_noise(t):
        t = t.lower()
        return any(x in t for x in [
            'click to register', 'online admission', 'registration',
            'contact us', 'sunbeam chambers', 'market yard road',
            'rajiv gandhi infotech park', 'all rights reserved'
        ])

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    SITEMAP = [
        ("COURSES", "Pre-CAT", "https://sunbeaminfo.in/pre-cat"),
        ("ABOUT", "About Sunbeam", "https://sunbeaminfo.in/about-us"),
        ("PLACEMENTS", "Placements", "https://sunbeaminfo.in/placements"),
        ("BRANCHES", "Hinjawadi", "https://sunbeaminfo.in/branch/hinjawadi"),
        ("BRANCHES", "Karad", "https://sunbeaminfo.in/branch/karad"),
    ]

    documents = []

    for section, title, url in SITEMAP:
        driver.get(url)
        time.sleep(4)

        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        collected = []

        for el in driver.find_elements(By.XPATH, "//h1|//h2|//h3|//p|//li"):
            text = clean_text(el.text)
            if len(text) > 30 and not is_noise(text):
                collected.append(text)

        page_text = "\n".join(dict.fromkeys(collected))

        if page_text:
            documents.append({
                "url": url,
                "content": page_text,
                "char_count": len(page_text),
                "source": "sunbeam",
                "scraper": "sitemap"
            })

        time.sleep(1)

    driver.quit()
    return documents
