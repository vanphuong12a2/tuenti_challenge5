import sys
from sets import Set
import itertools

def find_max_gold(elements):
   """Find max gold for a given elements"""

   # Initialize max gold as raw elements' gold
   max_gold = sum([values[e] for e in elements])

   # Loop through all combinations, check if new element create => call recursively for new list of elements 
   for s in xrange(2, len(elements)+1):
      for comb in itertools.combinations(elements, s):
         lcomb = list(comb)
         lcomb.sort()
         # Check if a combination can create a new element
         if ''.join(lcomb) in formulas:
            remain_elements = elements[:]
            for e in lcomb:
               remain_elements.remove(e)
            remain_elements.append(formulas[''.join(lcomb)])

            # Run recursively for the new list
            new_gold = find_max_gold(remain_elements)
            if max_gold < new_gold:
               max_gold = new_gold

   # When there is no new combination that create a element
   return max_gold

if __name__=="__main__":
   """ Solution for challenge 8 -  Alchemy Pot"""
    
   # Read data from book.data
   data_file = sys.argv[1]

   # Create a dictionary for formulas
   # key: string that joins all elements
   # value: the new element
   formulas = {}
   
   # Create a dictionary (element: gold)
   values = {}
   with open(data_file) as f:
      for line in f.readlines():
         info = line.split()                   
         values[info[0]] = int(info[1])
         if len(info) > 2:
            elements = info[2:]     
            elements.sort()
            formulas[''.join(elements)] = info[0]
 
   # Read N
   sys.stdin.readline()
 
   # Iterate each case
   for case in sys.stdin:
      elements = case.split()
      print find_max_gold(elements)
