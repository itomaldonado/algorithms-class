import sys, timeit, argparse
from functools import partial

# Naive implementation of the 3-sum algorithm, should be O(n^3)
def naive(filename=None):
  count = 0
  with open(filename) as f:
    int_list = f.readlines()
    for i in range(len(int_list)):
      for j in range (i+1,len(int_list)):
        for k in range(j+1,len(int_list)):
          if (int(int_list[i]) + int(int_list[j]) + int(int_list[k])) == 0:
            count += 1
  print "3-sum count:", count


if __name__ == '__main__':

  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Find 3-sum count in a list of integers provided via input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 1 time and get the exact time it takes to run this program
    times = timeit.Timer(partial(naive,args.file)).repeat(1,1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times) , 1.0) / 1.0
    print "Time taken: ", time_taken
  else:
    # We run it once just to get the actual 3-sum count value no runtime
    naive(args.file)

  
