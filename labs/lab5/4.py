def sort_tuple(lst):
    numbers = [x for x in lst if isinstance(x, (int, float))]
    return tuple(sorted(numbers))


x = [9, 0.66, "hello", "apps", 99, 14, None, "True"]
result = (tuple(x))
print(result)