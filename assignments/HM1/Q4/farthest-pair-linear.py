import sys, timeit, argparse
from functools import partial

# Linear implementation of the farthest pair, should be O(n)
# What we do is go through the array once looking for the min and max values
# Once we find the min and max value, these should be the farthest pair.
def farthest_pair_linear(filename=None):
  max_value = 0
  min_value = 0

  with open(filename) as f:
    float_list = f.readlines()
    if len(float_list) < 2: # if there is 1 or no items on the list, we don't bother...
      print 'No farthest pair.'
    else:
      # we initially set the max and min to the first value
      max_value = float(float_list[0])
      min_value = float(float_list[0])
      for f in float_list:
        f = float(f)
        if f > max_value:
          max_value = f
        elif f < min_value:
          min_value = f
  print "Farthest Pair:", str(max_value), ' -- ', str(min_value), ' -- Difference: ', str(max_value - min_value)


if __name__ == '__main__':

  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Find the farthest pair in a list of floats provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of floats', default='')
  
  # Get/parse arguments
  args = parser.parse_args()

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 1 time and get the exact time it takes to run this program
    times = timeit.Timer(partial(farthest_pair_linear,args.file)).repeat(1,1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times) , 1.0) / 1.0
    print "Time taken: ", time_taken
  else:
    # We run it once just to get the actual 3-sum count value no runtime
    farthest_pair_linear(args.file)

  
