import sys, timeit, argparse
from functools import partial

# Mergesort - Bottom-up approach, should be ~ O(N log N)
def mergesort(int_list):
  comps = 0
  int_list, comps = __sort_bottom_up(int_list, 0, len(int_list) - 1)
  return int_list, comps

# Internal representation of the sort portion of mergesort.
def __sort_bottom_up(a, low, high):
  comps = 0
  size = len (a)
  sas = 1 # this is the sub-array size, we are merging 2 arrays of about this size
  while sas < size: # while the sas is less than the whole array
    for i in xrange(0, size - sas, 2*sas): # we go from index 0 to 
      low = i
      mid = i + sas - 1
      high = min(i + 2*sas - 1, size - 1)
      a, temp = __merge(a, low, mid, high)
      comps += temp
    sas += sas
  return a, comps

# Internal representation of the merge portion of mergesort.
def __merge(a, low, mid, high):
  comps = 0
  aux = a[low:high+1] # get an auxiliary array, which is a slice of the original array from low to high
  lower_marker = 0 # starts at 0 because it is the lower bound of the aux array
  mid_marker = mid - low 
  upper_marker = mid_marker + 1
  
  # Start at the low bound of the original array
  i = low
  while i <= high: # while the 'i' marker is less or equal to the high bound:
    if lower_marker > mid_marker: # we ran out of lower ones, add the next upper one
      a[i] = aux[upper_marker]
      upper_marker += 1
    elif upper_marker >= len(aux): # we ran out of upper ones, add the next lower one
      a[i] = aux[lower_marker]
      lower_marker += 1
    elif aux[lower_marker] <= aux[upper_marker]: # lower one is less or equal to upper, use that
      a[i] = aux[lower_marker]
      lower_marker += 1
      comps += 1
    else: # else, just use the upper one
      a[i] = aux[upper_marker]
      upper_marker += 1
      comps += 1
    i += 1
  
  return a, comps


if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Sort a list of integers using mergesort (bottom-up), list is provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
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
    times = timeit.Timer( partial(mergesort, int_list) ).repeat(1, 1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 1.0
    print "Average Time taken: ", time_taken
  else:
    comps = 0
    # We run it once just to get the actual value
    int_list, comps = mergesort(int_list)

    # Print out the results to out.txt
    with open('./out.txt', 'wb') as f:
      f.write("%s" % comps)
      for item in int_list:
        f.write("\n%s" % item)


