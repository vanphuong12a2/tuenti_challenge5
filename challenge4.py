import sys
import base64
import struct


def decode(data, endian, reverse):
   """ Convert a bits string to inteter based on (endian+reverse) information"""
   if endian == 'L':
      split = [data[i*8:(i+1)*8] for i in range(len(data)//8+1)]
      data = ''.join(split[::-1])  
   if reverse: 
      data = data[::-1]
   
   return int('0b'+data, 2)

def process_line(bitstring, description):
   """Split the bitstring from decoded based on description"""

   # Extract information from description
   reverse = False
   if description[-1] == 'R':
      reverse = True
      description = description[:-1]
   endian = description[-1]
   bit_size = int(description[:-1])
  
   # Extract the bits string for each CPU
   sub_bitstring = bitstring[:bit_size]
   bitstring = bitstring[bit_size:]

   # Convert to integer
   res = decode(sub_bitstring, endian, reverse)  
  
   return res, bitstring

if __name__=="__main__":
   """ Solution for challenge 4 """

   # Read the first line
   sequence = sys.stdin.readline().strip()

   data = base64.standard_b64decode(sequence)

   bitstring = ''.join(['0' * (8-len(bin(ord(d))[2:])) + bin(ord(d))[2:]  for d in data])

   # Read the second line
   sys.stdin.readline()

   for line in sys.stdin:
      # Split the bitstring for each CPU
      description = line.strip()  
      res, bitstring = process_line(bitstring, description)
      print res
   

