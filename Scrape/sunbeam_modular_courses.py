def run_modular_courses_scraper():
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    documents = []

    def extract_all_text(container):
        texts = []
        elements = container.find_elements(
            By.XPATH,
            ".//*[self::p or self::li or self::td or self::th or self::div or self::span]"
        )
        for el in elements:
            t = el.text.strip()
            if t and len(t) > 20:
                texts.append(t)
        return "\n".join(dict.fromkeys(texts))

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    def create_driver():
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    index_driver = create_driver()
    wait = WebDriverWait(index_driver, 20)

    index_driver.get("https://sunbeaminfo.in/modular-courses-home")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "c_cat_box")))

    courses = []
    for card in index_driver.find_elements(By.CLASS_NAME, "c_cat_box"):
        title = card.find_element(By.CSS_SELECTOR, ".c_info h4").text.strip()
        link = card.find_element(By.CSS_SELECTOR, "a.c_cat_more_btn").get_attribute("href")
        courses.append((title, link))

    index_driver.quit()

    for course_title, course_url in courses:
        driver = None
        try:
            driver = create_driver()
            wait = WebDriverWait(driver, 20)

            driver.get(course_url)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "course_info")))
            time.sleep(2)

            info_box = driver.find_element(By.CLASS_NAME, "course_info")
            basic_text = extract_all_text(info_box)

            if basic_text:
                documents.append({
                    "url": course_url,
                    "content": basic_text,
                    "char_count": len(basic_text),
                    "course": course_title,
                    "section": "Basic Info",
                    "source": "sunbeam",
                    "scraper": "modular"
                })

            panels = driver.find_elements(By.CSS_SELECTOR, ".panel.panel-default")

            for panel in panels:
                try:
                    header = panel.find_element(By.CSS_SELECTOR, ".panel-title a")
                    section_name = header.text.strip()

                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});", header
                    )
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", header)
                    time.sleep(2.5)

                    body = panel.find_element(By.CLASS_NAME, "panel-body")
                    section_text = extract_all_text(body)

                    if not section_text:
                        section_text = body.text.strip()

                    if not section_text:
                        continue

                    documents.append({
                        "url": course_url,
                        "content": section_text,
                        "char_count": len(section_text),
                        "course": course_title,
                        "section": section_name,
                        "source": "sunbeam",
                        "scraper": "modular"
                    })

                except Exception:
                    continue

        except Exception:
            continue

        finally:
            if driver:
                driver.quit()

        time.sleep(1)

    return documents
