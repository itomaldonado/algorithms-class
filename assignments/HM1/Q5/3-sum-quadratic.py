import sys, timeit,argparse
from functools import partial

# Quadratic implementation of the 3-sum algorithm, should be O(N^2)
# Will use python's list.sort() function
def quadratic(filename=None):
  count = 0
  with open(filename) as f:
    int_list = [line.rstrip() for line in f]

    # Sort list
    int_list.sort()

    # Get list length
    size = len(int_list)

    # Using anchor + upper/lower bound to find the 3-sum
    # we go up from 0 to n-2 because we need a slot for the bounds
    for i in range(size - 1): # we move the anchor and try again from anchor+1 to the end.
      anchor = int(int_list[i])
      lower_bound = i+1
      upper_bound = size-1
      while upper_bound > lower_bound: # whle the upper and lower bounds don't cross eachother
        three_sum = anchor + int(int_list[lower_bound]) + int(int_list[upper_bound])
        if three_sum == 0: # we found a 3-sum, we mode the bounds one up/down
          count = count + 1
          lower_bound = lower_bound + 1
          upper_bound = upper_bound - 1
        elif three_sum < 0: # if the sum is under 0, we are under so we need a bigger lower bound value
          lower_bound = lower_bound + 1
        else: # we assume the sum is over 0, we are over so we need a smaller upper bound value
          upper_bound = upper_bound - 1

    print "3-sum count:",count

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
    times = timeit.Timer( partial(quadratic, args.file) ).repeat(1, 10)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times),1.0) / 10.0
    print "Average Time taken: ", time_taken
  else:
    # We run it once just to get the actual value
    quadratic(args.file)
    