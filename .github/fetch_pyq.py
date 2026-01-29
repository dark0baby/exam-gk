import requests
from bs4 import BeautifulSoup
import json, os
from datetime import date

DB_FILE = "data/gk_database.json"
today = date.today().isoformat()

os.makedirs("data", exist_ok=True)

# Example SSC CGL PYQ source (replace with actual)
SOURCES = [
    {
        "name": "SSC CGL PYQs",
        "url": "https://www.example.com/ssc-cgl-pyqs",
        "parser": "html"  # we'll use BeautifulSoup
    }
]

all_questions = []

# Load existing DB
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
else:
    db = []

existing_qs = [q["question"] for q in db]

for src in SOURCES:
    try:
        resp = requests.get(src["url"])
        soup = BeautifulSoup(resp.text, "lxml")

        # Example parsing logic — adjust based on actual website
        for block in soup.select(".question-block"):
            question = block.select_one(".q").text.strip()
            options = [opt.text.strip() for opt in block.select(".option")]
            answer = block.select_one(".answer").text.strip()
            topic = block.select_one(".topic").text.strip()
            notes = {opt: f"Short note for {opt}" for opt in options}

            if question not in existing_qs:
                all_questions.append({
                    "subject": topic,
                    "topic": topic,
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "notes": notes,
                    "source": src["name"]
                })
    except Exception as e:
        print(f"Failed to fetch {src['name']}: {e}")

db.extend(all_questions)

with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print(f"{len(all_questions)} new questions added on {today}")
