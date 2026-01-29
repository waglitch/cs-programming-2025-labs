def calculate_profit(a, n):
    if n <= 3:
        base_rate = 3.0
    elif n <= 6:
        base_rate = 5.0
    else:
        base_rate = 2.0
    bonus = min((a / 10_000) * 0.3, 5.0)
    rate = base_rate + bonus
    total = a
    for _ in range(n):
        total *= (1 + rate / 100)
    profit = total - a
    return round(profit, 2)
    
result = calculate_profit(10000, 4)
print(result) 