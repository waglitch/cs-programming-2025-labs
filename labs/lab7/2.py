staff_shifts = [
    {"name": "Dr. Shaw", "shift_cost": 120, "shifts": 15},
    {"name": "Agent Torres", "shift_cost": 90, "shifts": 22},
    {"name": "Researcher Hall", "shift_cost": 150, "shifts": 10}
]
total_costs = list(map(lambda emp: emp["shift_cost"] * emp["shifts"], staff_shifts))
print("\n2. Общая стоимость работы:")
print(total_costs)
print("Максимальная стоимость:", max(total_costs))