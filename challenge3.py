import sys

def primes(n):
   """ Returns  a list of primes < n """
   sieve = [True] * n
   for i in xrange(3,int(n**0.5)+1,2):
      if sieve[i]:
         sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
   return [2] + [i for i in xrange(3,n,2) if sieve[i]]
   
def count_primes(num, primes_list):
   """ Count number of repeatations for each prime in primes_list """
   counts = [0] * len(primes_list)
   for i, prime in enumerate(primes_list):
      while num%prime == 0:
         num = num/prime
         counts[i] += 1
   return counts
   
if __name__=="__main__":
   """ Solution for challenge 3 """

   # Get the numbers file
   numbers_file = sys.argv[1]
   with open(numbers_file) as f:
      numbers = [long(num) for num in f.readlines()]
      
   # Read the first line
   sys.stdin.readline()

   # Create a first 25 primes list
   primes_list = primes(100)
   
   counts = [count_primes(num, primes_list) for num in numbers]

   # Iterate the remaining lines
   for case in sys.stdin:
      ab = case.split()
      sub_counts = counts[int(ab[0]):int(ab[1])]
      final_counts = [sum(x) for x in zip(*sub_counts)]
      max_count = max(final_counts)
      popular_nums = [str(primes_list[i]) for i in range(len(primes_list)) if final_counts[i] == max_count]
      print max_count, ' '.join(popular_nums)
      

