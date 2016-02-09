import sys, timeit, argparse
from functools import partial

class QuickUnionBalancing:
  '''
  Quick union with balancing class.
  Inspired by the implementation in the class slides: 
  'fundamentals-1.pdf' 
  Provided by Dr. Jha
  '''

  # Initiate the arr of IDs with a specified max value, defaults to 8192
  def __init__(self, max_value=8192):
    self.arr = range(max_value) # initiate array with values 0..max_value-1
    self.size = [1] * max_value # initialize the size of the tree of all to '1' sinze they are all a tree with 1 element

  # Return the root of value
  def root(self, value):
    value = int(value)
    while (self.arr[value] != value):
      value = self.arr[value]
    return value

  # Return true if root(p) is the same as root(q
  def find(self, p, q):
    p = int(p)
    q = int(q)
    return self.root(p) == self.root(q)

  # Link p and q
  # Link root of smaller tree to the larger tree
  def union(self, p, q):
    p = int(p)
    q = int(q)
    root_p = self.root(p)
    root_q = self.root(q)
    if self.size[root_p] < self.size[root_q]: # if root of p is a smaller tree, link to root of q
      self.arr[root_p] = root_q
      self.size[root_q] = self.size[root_q] + self.size[root_p]
    else:
      self.arr[root_q] = root_p
      self.size[root_p] = self.size[root_q] + self.size[root_p]

# Read in the file, parse it, and go through it with QuickUnionBalancing
def quick_union_data(filename=None):
  count = 0
  qf = QuickUnionBalancing() # initialize the QuickUnionBalancing class
  with open(filename) as f:
    for line in f: # for each line
      line = line.rstrip('\n').rstrip('\r') # remove any new lines...
      ints = line.split(' ') # split the number pair into p and q
      if not qf.find(ints[0], ints[1]): # if p and q aren't connected, call union
        qf.union(ints[0],ints[1])
        print ints[0] + " " + ints[1] # print "p q"


if __name__ == '__main__':

  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Quick Union with Balancing algorithm ran from an input text file')
  parser.add_argument('-t', '--time', help='get run time in seconds', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integer pairs', default='')
  
  # Get/parse arguments
  args = parser.parse_args()

  # If the '--time' flag was given, we show the runtime of the program
  if args.time:
    # We use timeit to run this 1 time and get the exact time it takes to run this program
    times = timeit.Timer(partial(quick_union_data,args.file)).repeat(1,1)
    # Average time taken, divided by the number of repeats (since time is cumulative)
    time_taken = float(sum(times))/max(len(times) , 1.0) / 1.0
    print "Time taken: ", time_taken
  else:
    # We run it once just to get the actual 3-sum count value no runtime
    quick_union_data(args.file)

  
