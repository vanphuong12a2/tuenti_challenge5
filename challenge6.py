import sys
import numpy as np
from scipy import signal
 
def max_quality(y0, x0, y1, x1, K):
   """ Find the maximum quality airscrew """
   # Get the sub data
   subdata = data[y0:y1+1,x0:x1+1]

   # Calculate all the airscrews quality by convolving with the airscrews shape matrix
   windows = np.zeros((2*K+1,2*K+1))
   windows[:K,:K]= windows[-K:,-K:] = 1
   airscrews_quality = signal.fftconvolve(subdata, windows, mode='valid')

   # Extract the position of the maximum value (fftconvolve may not return the exact value due to float casting)
   position = airscrews_quality.argmax()
   x, y = position//airscrews_quality.shape[1], position%airscrews_quality.shape[1]
   row, col = x+K, y+K
    
   # Re-calculate the quality of the chosen position
   return np.sum(subdata[row-K:row, col-K:col]) + np.sum(subdata[row+1:row+K+1, col+1:col+K+1])
    
if __name__=="__main__":
   """ Solution for challenge 6 - Airscrews """
    
   data_file = sys.argv[1]
   with open(data_file) as f:
      f.readline()
      data = np.asarray([[int(num) for num in line.split()] for line in f.readlines()])
 
   # Read N
   sys.stdin.readline()
 
   # Iterate each case
   case_no = 1
   for case in sys.stdin:
      y0, x0, y1, x1, K = case.split()
      print 'Case ' + str(case_no) + ': ' + str(max_quality(int(y0), int(x0), int(y1), int(x1), int(K)))
      case_no += 1
