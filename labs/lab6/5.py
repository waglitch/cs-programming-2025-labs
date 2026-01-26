def is_palindrome(s):
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return "да" if cleaned == cleaned[::-1] else "нет"

result = is_palindrome(input(""))
print(result) 