def convert_time(value, from_unit, to_unit):
    secs = {'s': 1, 'm': 60, 'h': 3600}
    if from_unit not in secs or to_unit not in secs:
        raise ValueError("Use 's', 'm', or 'h'")
    return value * secs[from_unit] / secs[to_unit]

result = convert_time(60, 's', 'm')
print(result)