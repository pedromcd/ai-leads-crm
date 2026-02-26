import os, sqlite3
from collections import Counter

DB_PATH = os.getenv("DB_PATH", "../data/leads.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT intent, priority, score FROM leads")
rows = cur.fetchall()

print(f"Total leads: {len(rows)}")

intents = Counter(r[0] for r in rows)
priorities = Counter(r[1] for r in rows)
scores = [r[2] for r in rows if isinstance(r[2], int)]

print("\nLeads por intent:")
for k, v in intents.most_common():
    print(f"- {k}: {v}")

print("\nLeads por priority:")
for k, v in priorities.most_common():
    print(f"- {k}: {v}")

if scores:
    print(f"\nScore médio: {sum(scores)/len(scores):.1f}")