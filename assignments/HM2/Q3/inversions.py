import sys, timeit, argparse
from functools import partial

# Get number of inversions in list, The Kendall Tau distance implementation O(n lg n)
# We are assuming that the original location of all are 1...N
# N is the max number.
def inversions(arr):
  arr, inv = __inversions(arr, 0, len(arr) - 1)
  return inv

# Recursive inversion search, we will search half the array each time.
def __inversions(arr, start, end):
  inv = 0
  if start >= end: # done
    return arr, 0

  mid = start + (end - start) / 2
  arr, temp = __inversions(arr, start, mid)
  inv += temp
  arr, temp = __inversions(arr, (mid + 1), end)
  inv += temp
  arr, temp = __merge(arr, start, mid, end)
  inv += temp

  return arr, inv

# Do a merge, this is useful to know how many inversions we have
def __merge(arr, start, mid, end):
  inv = 0

  aux = arr[start:end+1] # get an auxiliary array, which is a slice of the original array from low to high

  lower_marker = 0
  mid_marker = mid - start 
  upper_marker = mid_marker + 1

  # Start at the low bound of the original array
  i = start
  while i <= end: # while the 'i' marker is less or equal to the high bound:
    if lower_marker > mid_marker: # we ran out of lower ones, add the next upper one
      arr[i] = aux[upper_marker]
      upper_marker += 1
    elif upper_marker >= len(aux): # we ran out of upper ones, add the next lower one
      arr[i] = aux[lower_marker]
      lower_marker += 1
    elif aux[lower_marker] <= aux[upper_marker]: # lower one is less or equal to upper, use that
      arr[i] = aux[lower_marker]
      lower_marker += 1
    else: # else, just use the upper one, this is an inversion, so we increase the counter
      arr[i] = aux[upper_marker]
      upper_marker += 1
      inv += 1
    i += 1

  return arr, inv

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Get the number of inversions in an integer list, list is provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing an ordered list of integers', default='')

  
  # Get/parse arguments
  args = parser.parse_args()

  # Parse/read in the while list, we don't want to take this time into account
  # when benchmarking the function
  int_list = []
  with open(args.file) as f:
    int_list = [int(line.rstrip()) for line in f]

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 'x' times and get the best time.
    times = timeit.Timer( partial(inversions, int_list) ).repeat(1, 1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 1.0
    print "Average Time taken: ", time_taken
  else:
    # We run it once just to get the actual value
    print inversions(int_list)

