def is_prime(n):
    if n <= 1:
        return False

    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False

    return True


try:
    s = input().strip()
    n = int(s)

    if is_prime(n):
        print("YES")
    else:
        print("NO")

except (ValueError, EOFError):
    print("NO")