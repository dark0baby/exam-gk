import requests
from bs4 import BeautifulSoup
import json, os
from datetime import date

DB_FILE = "data/gk_database.json"
today = date.today().isoformat()
os.makedirs("data", exist_ok=True)

# SSC/Bank PYQ sources
SOURCES = [
    {
        "name": "SSC CGL",
        "url": "https://sscportal.in/ssc-cgl-past-questions",
        "question_selector": ".q-block .q",
        "option_selector": ".q-block .option",
        "answer_selector": ".q-block .answer",
        "topic_selector": ".q-block .topic",
    },
    {
        "name": "SSC CHSL",
        "url": "https://sscportal.in/ssc-chsl-past-questions",
        "question_selector": ".q-block .q",
        "option_selector": ".q-block .option",
        "answer_selector": ".q-block .answer",
        "topic_selector": ".q-block .topic",
    },
    {
        "name": "SBI PO",
        "url": "https://www.sbi.co.in/careers/past-question-papers",
        "question_selector": ".q-block .q",
        "option_selector": ".q-block .option",
        "answer_selector": ".q-block .answer",
        "topic_selector": ".q-block .topic",
    }
]

# Load existing DB
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
else:
    db = []

existing_qs = [q["question"] for q in db]
new_questions = []

for src in SOURCES:
    try:
        r = requests.get(src["url"])
        soup = BeautifulSoup(r.text, "lxml")
        questions = soup.select(src["question_selector"])
        for i, q_el in enumerate(questions):
            question = q_el.get_text(strip=True)
            options = [opt.get_text(strip=True) for opt in soup.select(src["option_selector"])]
            answer = soup.select(src["answer_selector"])[i].get_text(strip=True)
            topic = soup.select(src["topic_selector"])[i].get_text(strip=True)
            notes = {opt: f"Note for {opt}" for opt in options}

            if question not in existing_qs:
                new_questions.append({
                    "subject": topic,
                    "topic": topic,
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "notes": notes,
                    "source": src["name"]
                })
    except Exception as e:
        print(f"Failed {src['name']}: {e}")

db.extend(new_questions)

with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print(f"Added {len(new_questions)} new questions on {today}")
