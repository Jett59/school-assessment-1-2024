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

try:
    limit = int(input("Semiprimes up to: "))
except ValueError:
    print("Invalid input")
    exit()

if limit < 1:
    print("Invalid input")
    exit()

primes = find_primes(limit // 2)

result = []

for i in range(len(primes)):
    for j in range(i, len(primes)):
        semiprime = primes[i] * primes[j]
        if semiprime <= limit:
            result.append(semiprime)
        else:
            break

if len(result) != 1:
    print(f"There are {len(result)} semiprimes below {limit}")
else:
    print(f"There is 1 semiprime below {limit}")

print(sorted(result))
