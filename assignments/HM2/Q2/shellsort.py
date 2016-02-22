import sys, timeit, argparse
from functools import partial

# Shell sort implementation
def shell_sort(int_list):
  comps = 0
  for h in (7 , 3 , 1):
    int_list, temp = __h_sort(int_list,h)
    comps += temp
  return int_list, comps

def __h_sort(a, h):
  comps = 0
  for curr_index in xrange(h, len(a), 1):
    swap_index = curr_index
    while (swap_index >= h):
      if a[swap_index] < a[swap_index - h]:
        temp = a[swap_index]
        a[swap_index] = a[swap_index - h]
        a[swap_index - h] = temp
        swap_index -= h
        comps += 1
      else: 
        break
  return a, comps

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Sort a list of integers using shell sort, list is provided via input text file')
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
    times = timeit.Timer( partial(shell_sort, int_list) ).repeat(1, 1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 1.0
    print "Average Time taken: ", time_taken
  else:
    comps = 0
    # We run it once just to get the actual value
    int_list, comps = shell_sort(int_list)

    # Print out the results to out.txt
    with open('./out.txt', 'wb') as f:
      f.write("%s" % comps)
      for item in int_list:
        f.write("\n%s" % item)
