scp_objects = [
    {"scp": "SCP-096", "class": "Euclid"},
    {"scp": "SCP-173", "class": "Euclid"},
    {"scp": "SCP-055", "class": "Keter"},
    {"scp": "SCP-999", "class": "Safe"},
    {"scp": "SCP-3001", "class": "Keter"}
]
enhanced = list(filter(lambda scp: scp["class"] != "Safe", scp_objects))
print("\n6. Усиленные меры содержания:")
print(enhanced)
