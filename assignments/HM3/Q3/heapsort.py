import sys, timeit, argparse, time
from functools import partial

def heapsort(int_list):
  """
  Heapsort implementation
  should be ~ O(N log N)
  """

  # Construct heap
  start = time.clock()
  length = len( int_list ) - 1
  for i in range ( (length / 2), -1, -1 ):
    int_list = __sink(int_list, i, length)
  
  # Contruction time
  c_time = time.clock() - start

  # Flatten heap into sorted array
  f_start = time.clock()
  for i in range (length, 0, -1):
    if int_list[0] > int_list[i]:
      __swap(int_list, 0, i)
      __sink(int_list, 0, i - 1)

  # Flatten time
  f_time = time.clock() - f_start

  # Total Time Taken:
  t_time = c_time + f_time
  
  print "%s,%s,%s" % (t_time, c_time, f_time)

  return int_list

def __sink(int_list, lower_bound, upper_bound):
  """
  Internal implementation of sinking a new root to its place
  """
  largest = 2 * lower_bound + 1
  while largest <= upper_bound:
    # If the right child exists and is larger than left child
    if ( largest < upper_bound ) and ( int_list[largest] < int_list[largest + 1] ):
      largest += 1
 
     # right child is larger than parent
    if int_list[largest] > int_list[lower_bound]:
      int_list = __swap( int_list, largest, lower_bound )
      # move down to largest child
      lower_bound = largest;
      largest = 2 * lower_bound + 1
    else:
      break
  return int_list


def __swap(int_list, a, b):
  """
  Swap two items in the list.
  """
  int_list[a], int_list[b] = int_list[b], int_list[a]
  return int_list

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Sort a list of integers using heapsort, list is provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()

  # Parse/read in the while list, we don't want to take this time into account
  # when benchmarking the function
  int_list = []
  with open(args.file) as f:
    int_list = [(line.rstrip()) for line in f]

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 'x' times and get the best time.
    times = timeit.Timer( partial(heapsort, int_list) ).repeat(1, 10)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 10.0
    print "Average Time taken: ", time_taken
  else:
    # We run it once just to get the actual value
    int_list = heapsort(int_list)

    first = True
    # Print out the results to out.txt
    with open('./out.txt', 'wb') as f:
      for item in int_list:
        if first:
          f.write("%s" % item)
          first = False
        else:
          f.write("\n%s" % item)
