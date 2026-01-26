def primes_in_range(a, b):
    if a > b:
        return "Error!"
    
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    primes = [n for n in range(a, b + 1) if is_prime(n)]
    return "Error!" if not primes else ' '.join(map(str, primes))
result = primes_in_range(1, 10)
print(result)