import json, os
from datetime import date
import random

DB_FILE = "data/gk_database.json"
TODAY = date.today().isoformat()
DATA_DIR = f"data/daily_tests/{TODAY}"
os.makedirs(DATA_DIR, exist_ok=True)
DAILY_FILE = f"{DATA_DIR}/daily_test.json"
INDEX_FILE = "index.json"

# Load GK DB
with open(DB_FILE, "r", encoding="utf-8") as f:
    db = json.load(f)

# Load index
if os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "r") as f:
        index = json.load(f)
else:
    index = {"daily": [], "weekly": {}, "monthly": {}, "yearly": []}

# Avoid repeating >20%
recent_questions = []
for day in index["daily"][-5:]:
    daily_file = f"data/daily_tests/{day}/daily_test.json"
    if os.path.exists(daily_file):
        with open(daily_file, "r") as f:
            recent_questions.extend([q["question"] for q in json.load(f)])

# Pick 15 questions, max 20% repeats
MAX_QUESTIONS = 15
today_questions = []

db_copy = db.copy()
random.shuffle(db_copy)

for q in db_copy:
    if len(today_questions) >= MAX_QUESTIONS:
        break
    if q["question"] in recent_questions and random.random() > 0.2:
        continue
    today_questions.append(q)

# Save daily JSON
with open(DAILY_FILE, "w", encoding="utf-8") as f:
    json.dump(today_questions, f, indent=2)

# Update index
index["daily"].append(TODAY)
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=4)

print(f"{len(today_questions)} questions generated for {TODAY}")
