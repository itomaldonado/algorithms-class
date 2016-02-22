import sys, timeit, argparse
from functools import partial

# Insertion sort implementation
def insertion_sort(int_list):
  comps = 0
  for anchor in xrange(0, len(int_list)):
    swap_index = anchor
    while (swap_index >= 1):
      if int_list[swap_index] < int_list[swap_index - 1]:
        temp = int_list[swap_index]
        int_list[swap_index] = int_list[swap_index - 1]
        int_list[swap_index - 1] = temp
        swap_index -= 1
        comps += 1
      else:
        break
  return int_list, comps

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Sort a list of integers using insertion sort, list is provided via input text file')
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
    times = timeit.Timer( partial(insertion_sort, int_list) ).repeat(1, 1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 1.0
    print "Average Time taken: ", time_taken
  else:
    comps = 0
    # We run it once just to get the actual value
    int_list, comps = insertion_sort(int_list)

    # Print out the results to out.txt
    with open('./out.txt', 'wb') as f:
      f.write("%s" % comps)
      for item in int_list:
        f.write("\n%s" % item)
