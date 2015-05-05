from __future__ import division
import sys
import numpy as np
import math
from scipy import signal
 
THRESCORR = 1e-30
 
def findScore(wave, pattern):
   """ Find maximum score for given wave and pattern """
   score = 0.
   minSubvectorLength = 2
   pattern = pattern - pattern.mean()
   # Recompute tasks to reduce the burden inside the loops
   patternSumCuadraticDiff = sum(np.power(pattern, 2))
        
   # Loop through the start position and length of the sub vector
   for subvectorStart in xrange(len(wave) - minSubvectorLength + 1):
      print subvectorStart
      for subvectorLength in xrange(minSubvectorLength, min(len(wave) - subvectorStart, len(pattern) + 1)):
         x = wave[subvectorStart:subvectorLength+subvectorStart]
         x = x - x.mean()
         denom = math.sqrt(sum(np.power(x,2)) * patternSumCuadraticDiff)
         if denom >= THRESCORR:
            # Use convolving function to slide the subvector through the pattern
            xcorrelation = signal.fftconvolve(pattern, x, mode='valid')
            score = max(score, (np.max(xcorrelation)/denom) * subvectorLength)
   return score
 
if __name__=="__main__":
   """ Solution for challenge 9 - X Correlate all the things """
  
   # Read P, W
   P, W = map(int, sys.stdin.readline().split())
 
   # Set up and save the vectors
   lines = sys.stdin.readlines()
   pattern = map(float, lines[:P])
   wave = map(float, lines[-W:])
   
   # Print the result and rounding 
   print("{0:.4f}".format(findScore(np.asarray(wave)[::-1], np.asarray(pattern))))
