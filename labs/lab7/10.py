evaluations = [
    {"name": "Agent Cole", "score": 78},
    {"name": "Dr. Weiss", "score": 92},
    {"name": "Technician Moore", "score": 61},
    {"name": "Researcher Lin", "score": 88}
]
best = max(evaluations, key=lambda e: e["score"])
print("\n10. Лучший сотрудник:")
print(f"{best['name']} - {best['score']} баллов")