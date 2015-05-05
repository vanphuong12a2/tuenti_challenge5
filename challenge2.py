import sys

def primes(n):
   """ Returns  a list of primes < n """
   sieve = [True] * n
   for i in xrange(3,int(n**0.5)+1,2):
      if sieve[i]:
         sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
   return [2] + [i for i in xrange(3,n,2) if sieve[i]]

def check_almost_prime(num, primes_list):
   """ Check if a number is almost prime """
   no_factors = 0
   max_prime = num - 1
   for prime in primes_list:
      if prime > max_prime:
         break
      while num % prime == 0:
         no_factors += 1
         num /= prime
      if no_factors > 2:
         return 0
   if no_factors == 2:
      return 1
   return 0

def count_almost_prime(a, b, primes_list):
   """ Count the number of almost prime numbers in the range [a,b] """
   count = 0
   for num in range(a, b+1):  
      count += check_almost_prime(num, primes_list)
   return count

if __name__=="__main__":
   """ Solution for challenge 2 """

   # Read the first line
   sys.stdin.readline()

   # Create a almost prime list in [2, 9999999]
   primes_list = primes(9999999)

   # Iterate the remaining lines
   for case in sys.stdin:
      ab = case.split()
      print count_almost_prime(int(ab[0]), int(ab[1]), primes_list)

