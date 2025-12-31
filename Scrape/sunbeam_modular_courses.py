def run_modular_courses_scraper():
    import time
    import io
    from contextlib import redirect_stdout

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    buffer = io.StringIO()
    documents = []

    with redirect_stdout(buffer):

        def extract_all_text(container):
            """
            Extracts text from p, li, td, th in correct order
            """
            texts = []
            elements = container.find_elements(
                By.XPATH,
                ".//*[self::p or self::li or self::td or self::th]"
            )
            for el in elements:
                t = el.text.strip()
                if t:
                    texts.append(t)
            return "\n".join(texts)

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        wait = WebDriverWait(driver, 40)

        driver.get("https://sunbeaminfo.in/modular-courses-home")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "c_cat_box")))

        courses = []
        for card in driver.find_elements(By.CLASS_NAME, "c_cat_box"):
            title = card.find_element(By.CSS_SELECTOR, ".c_info h4").text.strip()
            link = card.find_element(By.CSS_SELECTOR, "a.c_cat_more_btn").get_attribute("href")
            courses.append((title, link))

        for course_title, course_url in courses:
            driver.get(course_url)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "course_info")))
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            info_box = driver.find_element(By.CLASS_NAME, "course_info")
            basic_text = extract_all_text(info_box)

            documents.append({
                "content": basic_text,
                "course": course_title,
                "section": "Basic Info",
                "url": course_url,
                "source": "sunbeam",
                "scraper": "modular"
            })

            panels = driver.find_elements(By.CSS_SELECTOR, ".panel.panel-default")

            for panel in panels:
                try:
                    header = panel.find_element(By.CSS_SELECTOR, ".panel-title a")
                    section_name = header.text.strip()

                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", header)
                    time.sleep(0.5)

                    driver.execute_script("arguments[0].click();", header)
                    time.sleep(1.2)  

                    body = panel.find_element(By.CLASS_NAME, "panel-body")

                    section_text = extract_all_text(body)

                    if section_text:
                        documents.append({
                            "content": section_text,
                            "course": course_title,
                            "section": section_name,
                            "url": course_url,
                            "source": "sunbeam",
                            "scraper": "modular"
                        })

                except Exception:
                    continue

            time.sleep(1)

        driver.quit()

    return documents
