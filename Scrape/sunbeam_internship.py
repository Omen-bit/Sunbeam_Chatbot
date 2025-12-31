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

    title = soup.find("h1")
    if title:
        documents.append(f"[PAGE TITLE]\n{clean(title.get_text())}")

    for section in soup.find_all(["h2", "h3", "h4", "h5"]):
        section_text = [f"\n[{clean(section.get_text())}]"]

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

        documents.append("\n".join(section_text))

    for panel in soup.select(".panel-collapse"):
        accordion_block = []

        heading = panel.find_previous("h4")
        if heading:
            accordion_block.append(f"[{clean(heading.get_text())}]")

        for tag in panel.find_all(["p", "li"]):
            text = clean(tag.get_text())
            if text:
                accordion_block.append(text)

        if accordion_block:
            documents.append("\n".join(accordion_block))

    tables = soup.find_all("table")
    for idx, table in enumerate(tables, start=1):
        table_data = [f"[TABLE {idx}]"]

        headers = [clean(th.get_text()) for th in table.find_all("th")]
        if headers:
            table_data.append(" | ".join(headers))

        for row in table.find_all("tr"):
            cols = [clean(td.get_text()) for td in row.find_all("td")]
            if cols:
                table_data.append(" | ".join(cols))

        documents.append("\n".join(table_data))

    full_text = clean(soup.get_text())
    documents.append(f"[FULL PAGE TEXT]\n{full_text}")

    return documents
