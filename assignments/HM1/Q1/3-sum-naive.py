import sys, timeit
from functools import partial


# Check for arguments
if len(sys.argv) != 2:
  print 'Usage: python 3-sum-naive.py <path-to-input-data-file>'
  exit(1)

# Naive implementation of the 3-sum algorithm, should be O(n^3)
def naive(filename=None):
  count = 0
  with open(filename) as f:
    int_list = f.readlines()
    for i in range(0,len(int_list)):
      for j in range (i+1,len(int_list)):
        for k in range(j+1,len(int_list)):
          if (int(int_list[i]) + int(int_list[j]) + int(int_list[k])) == 0:
            count += 1
  return count


# Run the function defined above and get the best running time
if __name__ == '__main__':
  
  # We run it once just to get the actual value
  print "3-sum count: ",naive(sys.argv[1])

  # We use timeit to run this 'x' times and get the best time.
  times = timeit.Timer(partial(naive,sys.argv[1])).repeat(1,1)
  
  # Average time taken, divided by the number of repeats (since time is cumulative)
  time_taken = float(sum(times))/max(len(times),1) / 1
  
  print "Average Time taken: ", time_taken
