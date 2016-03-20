import sys, timeit, argparse
from functools import partial

# cutoff to insertion sort defaults to 0
cutoff = 0

# Mergesort To-Down Approach, should be ~ O(N log N)
def mergesort(int_list):
  int_list = __sort(int_list, 0, len(int_list) - 1)
  return int_list

# Internal representation of the sort portion of mergesort.
def __sort(a, low, high):  
  # if the high and low are crossed or the same, return, assumption: we are already "sorted"
  if low >= high:
    return a

  # Get the mid value doing int division, essentialy does a "floor" operation.
  mid = low + int((high - low) / 2)

  # Sort ech side of the array
  a = __sort(a, low, mid)
  a = __sort(a, mid + 1, high)
  a = __merge(a, low, mid, high)

  # Merge the sorted sides
  return a

# Internal representation of the merge portion of mergesort.
def __merge(a, low, mid, high):  
  if low >= high: # nothing to sort
    return a
  
  partition_size = ((high-low)+1)
  if partition_size <= cutoff: # cutoff for insertion sort
    a = __insertion_sort(a, low, high)
  else:
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
      else: # else, just use the upper one
        a[i] = aux[upper_marker]
        upper_marker += 1
      i += 1
  return a


# Insertion sort implementation
def __insertion_sort(int_list, low, high):
  for anchor in xrange(low, (high+1)):
    swap_index = anchor
    while (swap_index >= 1):
      if int_list[swap_index] < int_list[swap_index - 1]:
        temp = int_list[swap_index]
        int_list[swap_index] = int_list[swap_index - 1]
        int_list[swap_index - 1] = temp
        swap_index -= 1
      else:
        break
  return int_list


if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Sort a list of integers using mergesort top-down, list is provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('-c', '--cutoff', help='cutoff value for insertion sort', default=0)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()

  # Parse/read in the while list, we don't want to take this time into account
  # when benchmarking the function
  int_list = []
  with open(args.file) as f:
    int_list = [int(line.rstrip()) for line in f]

  # update cutoff
  cutoff = int(args.cutoff)

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 'x' times and get the best time.
    times = timeit.Timer( partial(mergesort, int_list) ).repeat(1, 10)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 10.0
    print "Average Time taken: ", time_taken
  else:
    # We run it once just to get the actual value
    int_list = mergesort(int_list)

    # Print out the results to out.txt
    first = True
    with open('./out.txt', 'wb') as f:
      for item in int_list:
        if first:
          f.write("%s" % item)
          first = False
        else:
          f.write("\n%s" % item)
