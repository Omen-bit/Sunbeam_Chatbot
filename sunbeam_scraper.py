import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

print("Opening homepage...")
driver.get("https://sunbeaminfo.in/index")
time.sleep(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(2)

cards = driver.find_elements(By.CSS_SELECTOR, "div.course_box")

links = []

for card in cards:
    title = card.find_element(By.TAG_NAME, "h4").text.strip()
    link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
    links.append((title, link))

static_links = [
    ("About Sunbeam", "https://sunbeaminfo.in/about-us"),
    ("Branches Home", "https://sunbeaminfo.in/sunbeam-branches-home"),
    ("Branch Pune - Hinjawadi", "https://sunbeaminfo.in/branch/hinjawadi"),
    ("Branch Pune - Market Yard", "https://sunbeaminfo.in/branch/pune"),
]

links.extend(static_links)
driver.quit()

print("All links found:")
for l in links:
    print(l)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SunbeamBot/1.0)"
}


def is_noise(text: str) -> bool:
    noise_patterns = [
        "registration",
        "online admission",
        "contact us",
        "©",
        "all rights reserved",
        "sunbeam chambers",
        "sunbeam it park",
        "market yard road",
        "rajiv gandhi infotech park",
        "pune -",
        "+91",
        "powered by",
        "designed by",
        "follow us",
        "facebook",
        "twitter",
        "linkedin",
        "instagram"
    ]
    t = text.lower()
    return any(p in t for p in noise_patterns)


def scrape_page(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup([
        "script", "style", "noscript", "svg",
        "header", "footer", "nav", "aside",
        "form", "iframe"
    ]):
        tag.decompose()

    extracted = []
    seen = set()

    for h in soup.find_all(["h1", "h2", "h3"]):
        text = h.get_text(strip=True)
        if len(text) >= 4 and not is_noise(text) and text not in seen:
            extracted.append(f"\n## {text}")
            seen.add(text)

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) >= 30 and not is_noise(text) and text not in seen:
            extracted.append(text)
            seen.add(text)

    for li in soup.find_all("li"):
        text = li.get_text(strip=True)
        if len(text) >= 25 and not is_noise(text) and text not in seen:
            extracted.append(f"- {text}")
            seen.add(text)

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cols = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
            if len(cols) >= 2:
                row_text = " | ".join(cols)
                if not is_noise(row_text) and row_text not in seen:
                    extracted.append(row_text)
                    seen.add(row_text)

    return "\n".join(extracted)


print("Starting background scraping...")

for title, link in links:
    print("=" * 80)
    print(f"Page: {title}")
    print(f"URL: {link}\n")

    try:
        content = scrape_page(link)
        print(content)
    except Exception as e:
        print(f"Failed to scrape {link}")
        print(e)

print("DONE")
