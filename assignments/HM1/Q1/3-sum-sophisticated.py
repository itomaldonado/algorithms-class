import sys, timeit,argparse
from functools import partial

# Sophisticated implementation of the 3-sum algorithm, should be O(N^2 log N)
# Will use python's list.sort() function
def sophisticated(filename=None):
  count = 0
  with open(filename) as f:
    int_list = [line.rstrip() for line in f]

    # Sort list
    int_list.sort()

    # Use binary search to find the 3-sum
    for i in range(len(int_list)-1):
      for j in range(len(int_list)-1):
        search_index = binary_search(int_list, 0, len(int_list)-1, int( -1 * ( int(int_list[i]) + int(int_list[j]) )))
        if search_index > -1:
          if int(int_list[i]) < int(int_list[j]) and int(int_list[j]) < int(int_list[search_index]):
            count += 1
    print "3-sum count:",count

# Recursive binary search implementation, returns -1 if item not found in the list
def binary_search(alist, first, last, item):
  # Get the mid item
  mid = ( (last - first) // 2 ) + first
  if int(alist[mid]) == int(item): # If the mid item is the one we want, return it.
    return mid
  elif first >= last: # If the current item is not what we want and we reached the end of the list, we return -1
    return -1
  elif int(alist[mid]) < int(item): # If the mid item is larger, we search from mid+1 to last 
    return binary_search(alist, mid+1, last, item)
  elif int(alist[mid]) > int(item): # If the mid item is larger, we search from first to mid-1
    return binary_search(alist, first, mid-1, item)


if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Find 3-sum count in a list of integers provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 'x' times and get the best time.
    times = timeit.Timer( partial(sophisticated, args.file) ).repeat(1, 1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 1.0
    print "Average Time taken: ", time_taken
  else:
    # We run it once just to get the actual value
    sophisticated(args.file)