def run_internship_scraper():
    import requests
    from bs4 import BeautifulSoup

    URL = "https://www.sunbeaminfo.in/internship"

    def clean(text):
        return " ".join(text.replace("\xa0", " ").split())

    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    documents = []

    page_blocks = []

    title = soup.find("h1")
    if title:
        page_blocks.append(clean(title.get_text()))

    for section in soup.find_all(["h2", "h3", "h4", "h5"]):
        section_text = [clean(section.get_text())]

        nxt = section.find_next_sibling()
        while nxt and nxt.name not in ["h2", "h3", "h4", "h5"]:
            if nxt.name == "p":
                text = clean(nxt.get_text())
                if text:
                    section_text.append(text)
            elif nxt.name == "ul":
                for li in nxt.find_all("li"):
                    section_text.append(f"- {clean(li.get_text())}")
            nxt = nxt.find_next_sibling()

        page_blocks.append("\n".join(section_text))

    full_text = "\n\n".join(page_blocks)

    documents.append({
        "url": URL,
        "content": full_text,
        "char_count": len(full_text),
        "source": "sunbeam",
        "scraper": "internship"
    })

    return documents
