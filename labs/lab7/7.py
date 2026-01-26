incidents = [{"id": 101, "staff": 4}, {"id": 102, "staff": 12}, {"id": 103, "staff": 7}, {"id": 104, "staff": 20}]
top_three = sorted(incidents, key=lambda x: x["staff"], reverse=True)[:3]
print("\n7. Топ-3 инцидента:")
print(top_three)
