def run_sunbeam_scraper():
    import time
    import re
    import io
    from contextlib import redirect_stdout

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager


    buffer = io.StringIO()   
    with redirect_stdout(buffer):   

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
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.set_page_load_timeout(60)

        SITEMAP = [
            ("COURSES", "Pre-CAT", "https://sunbeaminfo.in/pre-cat"),
            ("COURSES", "Mastering MCQs", "https://sunbeaminfo.in/modular-courses.php?mdid=57"),
            ("COURSES", "Modular Courses", "https://sunbeaminfo.in/modular-courses-home"),
            ("ABOUT", "About Sunbeam", "https://sunbeaminfo.in/about-us"),
            ("PLACEMENTS", "Placements", "https://sunbeaminfo.in/placements"),
            ("BRANCHES", "Branches Home", "https://sunbeaminfo.in/sunbeam-branches-home"),
            ("BRANCHES", "Pune - Hinjawadi", "https://sunbeaminfo.in/branch/hinjawadi"),
            ("BRANCHES", "Pune - Market Yard", "https://sunbeaminfo.in/branch/pune"),
            ("BRANCHES", "Karad", "https://sunbeaminfo.in/branch/karad"),
        ]

        def scrape(section, title, url):
            print("\n" + "=" * 100)
            print(section)
            print(f"Page: {title}")
            print(f"URL: {url}")
            print("=" * 100)

            try:
                driver.get(url)
                time.sleep(5)
            except:
                time.sleep(3)

            for _ in range(4):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

            expand_selectors = [
                "[data-toggle='collapse']",
                "a[href^='#']",
                ".collapsed",
                "[aria-expanded='false']"
            ]

            clicked = set()
            for selector in expand_selectors:
                for el in driver.find_elements(By.CSS_SELECTOR, selector):
                    try:
                        key = el.get_attribute("outerHTML")[:100]
                        if key not in clicked:
                            driver.execute_script("arguments[0].click();", el)
                            clicked.add(key)
                            time.sleep(0.3)
                    except:
                        pass

            seen = set()
            out = []

            def add(x):
                if x and x not in seen:
                    seen.add(x)
                    out.append(x)

            for h in driver.find_elements(By.XPATH, "//h1|//h2|//h3"):
                t = clean_text(h.text)
                if len(t) > 3 and not is_noise(t):
                    add(t.upper())

            for p in driver.find_elements(By.TAG_NAME, "p"):
                t = clean_text(p.text)
                if len(t) > 40 and not is_noise(t):
                    add(t)

            for ul in driver.find_elements(By.TAG_NAME, "ul"):
                if 'nav' in (ul.get_attribute("class") or '').lower():
                    continue
                for li in ul.find_elements(By.TAG_NAME, "li"):
                    t = clean_text(li.text)
                    if len(t) > 15 and not is_noise(t):
                        add(f"- {t}")

            for table in driver.find_elements(By.TAG_NAME, "table"):
                rows = []
                for r in table.find_elements(By.TAG_NAME, "tr"):
                    cells = [
                        clean_text(c.text)
                        for c in r.find_elements(By.XPATH, ".//th|.//td")
                        if c.text.strip()
                    ]
                    if cells:
                        rows.append(" | ".join(cells))
                if rows:
                    add("TABLE:")
                    for r in rows:
                        add(r)

            print("\n".join(out))

        print("Starting sitemap-based scraping...\n")

        for s, t, u in SITEMAP:
            scrape(s, t, u)
            time.sleep(2)

        driver.quit()
        print("\nSCRAPING COMPLETED SUCCESSFULLY")

    raw_text = buffer.getvalue()

    documents = [
        block.strip()
        for block in raw_text.split("=" * 100)
        if block.strip()
    ]

    return documents
