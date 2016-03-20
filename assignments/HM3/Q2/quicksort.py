import sys, timeit, argparse
from functools import partial

def quicksort(int_list):
  """
  Quicksort implementation with median-of-three approach
  should be ~ O(N log N)
  """
  comps = 0
  int_list, comps = __sort(int_list, 0, len(int_list) - 1)
  return int_list, comps

def __sort(int_list, lower_bound, upper_bound):
  """
  Internal implementation of quicksort
  Implemented recusively
  """
  comps = 0
  if lower_bound >= upper_bound: # nothing to sort
    return int_list, comps
  else:
    # Get median of three as the pivot
    low = {'index': lower_bound, 'value': int_list[lower_bound]}
    high = {'index': upper_bound, 'value': int_list[upper_bound]}
    center = {'index': int((upper_bound + lower_bound) / 2), 'value': int_list[ int((upper_bound + lower_bound) / 2) ]}
    mean_of_three = __mean3(low,center,high)
    pivot = mean_of_three['index']

    # swap lower_bound element with pivot before partitioning
    int_list = __swap(int_list, lower_bound, pivot)
    
    # Partition the list
    int_list, temp, j = __partition(int_list, lower_bound, upper_bound)
    comps += temp
    
    # Sort left side
    int_list, temp = __sort(int_list, lower_bound, int(j-1))
    comps += temp

    # Sort right side
    int_list, temp = __sort(int_list, int(j+1), upper_bound)
    comps += temp

    return int_list, comps

def __partition(int_list, lower_bound, upper_bound):
  """
  Partition the subarray int_list[lower_bound ... upper_bound] so that 
  int_list[lower_bound ... j-1] <= int_list[j] and
  int_list[j] <= int_list[j+1 ... upper_bound]
  """
  comps = 0
  i = lower_bound + 1
  j = upper_bound
  p = int_list[lower_bound]
  while True:
    # find item on lower_bound to swap
    while int_list[i] <= p: # while item is less or equal to pivot
      comps +=1 # increase comparisons
      if upper_bound == i:
        break
      else:
        i += 1

    # find item on hi to swap
    while int_list[j] >= p: # while item is higher or equal than pivot
      comps +=1 # increase comparisons
      if j == lower_bound:
        break #redundant since a[lo] acts as sentinel
      else:
        j -= 1

    if i >= j: # if pointers cross, break!
      break

    int_list = __swap(int_list, i, j)

  # put pivot item p at int_list[j]
  int_list = __swap(int_list, lower_bound, j);

  # we return 'j' because
  # int_list[lower_bound ... j-1] <= int_list[j] and
  # int_list[j] <= int_list[j+1 ... upper_bound]
  return int_list, comps, j


def __swap(int_list, a, b):
  """
  Swap two items in the list.
  """
  int_list[a], int_list[b] = int_list[b], int_list[a]
  return int_list


def __mean3(a, b, c):
  """
  Calculate the mean of three
  accepts three dicts with structure {index: int, value: comparable}
  Returns the dicts with the mean value
  """
  if a['value'] <= b['value'] <= c['value'] or c['value'] <= b['value'] <= a['value']:
    return b
  elif b['value'] <= a['value'] <= c['value'] or c['value'] <= a['value'] <= b['value']:
    return a
  else:
    return c


if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Sort a list of integers using quicksort median-of-three, list is provided via input text file')
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
    times = timeit.Timer( partial(quicksort, int_list) ).repeat(1, 10)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 10.0
    print "Average Time taken: ", time_taken
  else:
    comps = 0
    # We run it once just to get the actual value
    int_list, comps = quicksort(int_list)

    first = True
    # Print out the results to out.txt
    with open('./out.txt', 'wb') as f:
      for item in int_list:
        if first:
          f.write("%s" % item)
          first = False
        else:
          f.write("\n%s" % item)
