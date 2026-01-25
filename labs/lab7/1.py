objects = [("Containment Cell A", 4), ("Archive Vault", 1), ("Bio Lab Sector", 3), ("Observation Wing", 2)]
print("1. Сортировка по уровню угрозы:")
print(sorted(objects, key=lambda x: x[1]))