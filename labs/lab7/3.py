personnel = [
    {"name": "Dr. Klein", "clearance": 2},
    {"name": "Agent Brooks", "clearance": 4},
    {"name": "Technician Reed", "clearance": 1}
]
personnel_cat = list(map(lambda p: {
    "name": p["name"], 
    "clearance": p["clearance"],
    "category": "Restricted" if p["clearance"] == 1 
                else "Confidential" if p["clearance"] in [2, 3] 
                else "Top Secret"
}, personnel))
print("\n3. Категории допуска:")
print(personnel_cat)