# We use a simple sieve of Eratosthenes algorithm to find the primes up to limit/2.
# We use limit/2 because we need to find semiprimes up to limit, and that means we multiply the primes by at least 2.
# Once we have the primes, we just go through the list, multiplying pairs together.
# To avoid duplicates (2*3 = 3*2 for example), we only ever select numbers that are greater than or equal to the first number to be the second number.

def check_divisibility(n, primes):
    for prime in primes:
        if prime > n:
            return False
        if n % prime == 0:
            return True
    return False

def find_primes(limit):
    primes = [2, 3]
    # For performance, we use the fact that all primes are of the form 6n+1 or 6n-1.
    for n in range(1, (limit + 1) // 6 + 1):
        candidate = 6 * n - 1
        if not check_divisibility(candidate, primes):
            primes.append(candidate)
        candidate = 6 * n + 1
        if not check_divisibility(candidate, primes):
            primes.append(candidate)
    return primes

def find_semiprimes(min, max):
    primes = find_primes(max // 2)
    result = []

    for i in range(len(primes)):
        for j in range(i, len(primes)):
            semiprime = primes[i] * primes[j]
            if semiprime <= max:
                if semiprime >= min:
                    result.append(semiprime)
            else:
                break # The next primes are all larger, so they will all be too big.
    return result

try:
    min = int(input("Min: "))
    max = int(input("Max: "))
except ValueError:
    print("Invalid input")
    exit()

if min > max or max < 1:
    print("Invalid input")
    exit()

semiprimes = find_semiprimes(min, max)

if len(semiprimes) != 1:
    print(f"There are {len(semiprimes)} semiprimes between {min} and {max}")
else:
    print(f"There is 1 semiprime between {min} and {max}")

print(sorted(semiprimes))
