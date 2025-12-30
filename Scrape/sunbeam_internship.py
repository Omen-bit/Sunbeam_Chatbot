def run_internship_scraper():
    import requests
    from bs4 import BeautifulSoup

    URL = "https://www.sunbeaminfo.in/internship"

    def clean(text):
        return " ".join(text.split())

    def scrape_internships():
        response = requests.get(URL, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        documents = []

        intro = soup.find("div", class_="container")
        if intro:
            for p in intro.find_all("p"):
                text = clean(p.get_text())
                if len(text) > 80:
                    documents.append(f"[INTERNSHIP OVERVIEW]\n{text}")

        accordions = soup.find_all("div", class_="panel-collapse")
        for acc in accordions:
            section_text = []

            for h in acc.find_all(["h3", "h4", "h5"]):
                section_text.append(h.get_text(strip=True))

            for p in acc.find_all("p"):
                text = clean(p.get_text())
                if len(text) > 40:
                    section_text.append(text)

            for ul in acc.find_all("ul"):
                for li in ul.find_all("li"):
                    li_text = clean(li.get_text())
                    if len(li_text) > 20:
                        section_text.append(f"- {li_text}")

            if section_text:
                documents.append("\n".join(section_text))

        table1 = soup.find("div", id="collapseSix")
        if table1:
            for row in table1.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 5:
                    documents.append(
                        f"""
Technology: {cols[0].get_text(strip=True)}
Aim: {cols[1].get_text(strip=True)}
Prerequisite: {cols[2].get_text(strip=True)}
Learning: {cols[3].get_text(strip=True)}
Location: {cols[4].get_text(strip=True)}
""".strip()
                    )

        table2 = soup.find("div", class_="table-responsive")
        if table2:
            for row in table2.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 7:
                    documents.append(
                        f"""
Batch: {cols[1].get_text(strip=True)}
Duration: {cols[2].get_text(strip=True)}
Start Date: {cols[3].get_text(strip=True)}
End Date: {cols[4].get_text(strip=True)}
Time: {cols[5].get_text(strip=True)}
Fees: {cols[6].get_text(strip=True)}
""".strip()
                    )

        return documents

    return scrape_internships()
