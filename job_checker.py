import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzFmT1zVQPYWtQgqCuGvP418C0UtZgq5EYrSM_dyLvmlnvTMU2KUq5Ik38RHOSQr06S/exec"

EXCLUDED_KEYWORDS = [
    "engineer",
    "software",
    "backend",
    "frontend",
    "full-stack",
    "machine learning",
    "data scientist",
    "devops",
    "security",
    "infrastructure"
]

COMPANY_PAGES = {
    "Amazon": "https://www.amazon.jobs/en/search?base_query=&loc_query=United%20States",
    "Google": "https://careers.google.com/jobs/results/",
    "Apple": "https://jobs.apple.com/en-us/search",
    "Fanatics": "https://www.fanaticsinc.com/careers",
    "Overtime": "https://boards.greenhouse.io/overtime",
    "NFL": "https://www.teamworkonline.com/football-jobs/nfl",
    "LIV Golf": "https://www.teamworkonline.com/golf-jobs",
}

def is_allowed(title):
    title = title.lower()
    return not any(word in title for word in EXCLUDED_KEYWORDS)

def main():
    jobs = []
    today = datetime.today().strftime("%Y-%m-%d")

    for company, url in COMPANY_PAGES.items():
        try:
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")

            for link in soup.find_all("a"):
                title = link.get_text(strip=True)
                href = link.get("href")

                if not title or not href:
                    continue

                if not href.startswith("http"):
                    href = url + href

                if is_allowed(title):
                    jobs.append({
                        "date": today,
                        "company": company,
                        "title": title,
                        "location": "",
                        "link": href
                    })

        except:
            continue

    if jobs:
        requests.post(WEB_APP_URL, data=json.dumps(jobs))

if __name__ == "__main__":
    main()
