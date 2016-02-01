import sys, timeit
from functools import partial


# Check for arguments
if len(sys.argv) != 2:
  print 'Usage: python 3-sum-naive.py <path-to-input-data-file>'
  exit(1)

# Sophisticated implementation of the 3-sum algorithm, should be O(N^2 lg N)
# Will use python's list.sort() function
def sophisticated(filename=None):
  count = 0
  with open(filename) as f:
    int_list = [line.rstrip() for line in f]

    # Sort list
    int_list.sort()

    # Use binary search to find the 3-sum
    for i in range(0,len(int_list)-1):
      for j in range(0,len(int_list)-1):
        search_index = binary_search(int_list, 0, len(int_list)-1, int( -1 * ( int(int_list[i]) + int(int_list[j]) )))
        if search_index > -1:
          if int(int_list[i]) < int(int_list[j]) and int(int_list[j]) < int(int_list[search_index]):
            count += 1
    return count

# Binary search implementation, returns -1 if item not found in the list
def binary_search(alist, first, last, item):
  mid = ( (last - first) // 2 ) + first
  if int(alist[mid]) == int(item):
    return mid
  elif first >= last: # If the current item is not what we want and we reached the end of the list, we return -1
    return -1
  elif int(alist[mid]) < int(item):
    return binary_search(alist, mid+1, last, item)
  elif int(alist[mid]) > int(item): 
    return binary_search(alist, first, mid-1, item)

# Run the function defined above and get the best running time
if __name__ == '__main__':
  
  # We run it once just to get the actual value
  count = sophisticated(sys.argv[1])
  print "3-sum count: ", count

  # We use timeit to run this 'x' times and get the best time.
  number_per_iteration = 1
  total_iteration = 1
  times = timeit.Timer( partial(sophisticated, sys.argv[1]) ).repeat(number_per_iteration, total_iteration)
  
  # Average time taken, divided by the number of repeats (since time is cumulative)
  time_taken = float(sum(times))/max(len(times),1) / total_iteration
  
  print "Average Time taken: ", time_taken
