import sys, timeit, argparse, time, random
from functools import partial
from math import sqrt

###############
# Increasing the recursion limit since we will be doing recursive puts on a tree
sys.setrecursionlimit(10**6)
###############

# For logging
LOG_ENABLED = False

# For colors
RED = True
BLACK = False

def new_node(key=None, val=None, left=None, right=None, N=0, color=BLACK):
  """
  Create a new node structure
  """
  new_node = {
    'key': key,
    'val': val,
    'left': left,
    'right': right,
    'N': N,
    'color': color # False == Black, True == Red
  }
  return new_node

class RBT:
  """
  Implementation of 2-3 Trees using Red-Black Trees
  For this case, NO re-balancing is done
  
  A node is a dict of:
  {
    'key' --> sorted by key
    'val' --> associated data
    'left' --> left subtree
    'right' --> right subtree
    'N' --> number of nodes in subtree
    color --> False == Black, True == Red
  }
  """

  def __init__(self):
    """
    Initialize the RBT class
    """
    self.root = None

  def empty(self):
    """
    returns true if RBT is of size 0
    """
    return self.size() == 0

  def size(self):
    """
    Returns the size of the RBT
    """
    return self.__size(self.root)

  def __size(self, node):
    """
    Private method, returns size of a specific node
    """
    if node == None:
      return 0
    
    return node['N']

  def path(self, key):
    """
    Return the path length to a given key
    """
    value, path_lenght = self.__get(self.root, key)
    return path_lenght

  def get(self, key):
    """
    Get the value associated with a given key starting at the given node
    Return 'None' if key does not exist
    """
    value, path_lenght = self.__get(self.root, key)
    return value

  def __get(self, node, key):
    """
    Get the value associated with a given key
    If Node is 'None' return 'None'
    If key is smaller than node, search left subtree
    If key is larger than node, search right subtree
    If key is the same as node, return node value
    """
    temp = 0
    path = 0
    value = None 
    if node is None:
      value = None
    elif key < node['key']:
      path += 1
      value, temp = self.__get(node['left'], key)
    elif key > node['key']:
      path += 1
      value, temp = self.__get(node['right'], key)
    else:
      value = node['val']

    path += temp
    return value, path

  def put(self, key, val):
    """
    Put the key,value in the RBT
    Raise exception if key is None
    Delete key if value is None
    """
    if key == None:
      raise Exception("key is None")
    if val == None:
      self.delete(key)
      return None
    self.root = self.__put(parent=None, node=self.root, key=key, val=val)

  def __put(self, parent, node, key, val):
    """
    Private implementation of put.
    If node is None, create a new node with key, val of node count of 1
    If key is smaller than node, put the new node in the left subtree
    If key is larger than node, put the new node in the right subtree
    If keys equal, change the value of this node
    DO NOT REBALANCE
    Finally, update the node's count
    """
    if (self.__red(parent) is not True) and (node is None): # if parent is 2-node, insert red link
      return new_node(key=key, val=val, N=1, color=RED)
    elif (self.__red(parent) is True) and (node is None):
      return new_node(key=key, val=val, N=1, color=BLACK) # if parent is 3-node, insert black link
    elif key < node['key']:
      node['left'] = self.__put(parent=node, node=node['left'], key=key, val=val)
    elif key > node['key']:
      node['right'] = self.__put(parent=node, node=node['right'], key=key, val=val)
    else:
        node['val'] == val

    # We do NOT perform re-balancing operations

    node['N'] = 1 + self.__size(node['left']) + self.__size(node['right'])
    return node

  ### RedBlack Tree Helper Functions

  def red(self, node):
    return self.__red(node)

  def __red(self, node):
    """
    Returns true if node is red
    """
    if node is None:
      return BLACK
    return node['color'] == RED

# Helper function to calculate the mean and standard deviation
def mean_std_dev(data):
  """ Calculate mean and standard deviation of data []: """
  length, mean, std = len(data), 0, 0
  for item in data:
      mean = mean + item
  mean = mean / float(length)
  for item in data:
      std = std + (item - mean) ** 2
  std = sqrt(std / float(length))
  mean = int(round(mean))
  std = int(round(std))
  return mean, std

# Logging Helper function
def log(txt):
  if LOG_ENABLED:
    print(txt)

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Red-Black Tree implementation, list is randomly generated')
  parser.add_argument('-t', '--trials', help='number of trials', default=100)
  parser.add_argument('-s', '--sorted', help='Preform sorted insertions', action='store_true', default=False)
  parser.add_argument('-l', '--log', help='Print trial stats', action='store_true', default=False)

  #parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()
  LOG_ENABLED = args.log
  trials = int(args.trials)
  sorted_insertions = args.sorted
  sizes = [10, 100, 1000, 10000]


  # Start Trials
  # For each size, run 'args.trials' trials
  # Writes to ./out.txt the mean and standard deviation of path length per size
  with open('./out.txt', 'wb') as f:
    f.write( "size,sorted,mean,standard_deviation\n" )
    log ("=================================")
    for size in sizes: # for each trial size
      # Keep track path lengths
      lengths = list()
      for trial in range(1, trials+1): # for each trial in size
        # Print trial number
        log("Size: {0}, Trial: {1}".format(size, trial))
        # Generate new random List
        start = time.clock()
        int_list = [i for i in range(size)]
        if not sorted_insertions: # if not doing sorted insertions, shuffle the array
          random.shuffle(int_list)
        log ( 'List Generation Time: {0}'.format( (time.clock() - start) ) )
        # Build Red-Black Tree
        start = time.clock()
        rbt = RBT()
        for item in int_list:
          rbt.put(item,item)
        log ( 'RBT Generation Time: {0}'.format( (time.clock() - start) ) )
        # Get Path length to random element
        element = random.randrange(1, size+1) # get a random element key
        path_length = rbt.path(element) # calculate path length
        log ( "Random Element: {0}, Path Length: {1}".format(element,path_length))
        log ( 'Path Length Calculation Time: {0}'.format( (time.clock() - start) ) )
        # Add path length to list of path lengths
        lengths.append(path_length)
        log ("---------------------------------")
      # Print mean and standard deviation for all trials in the current size
      mean, std = mean_std_dev(lengths)
      # Print out the results to out.txt
      final_stat = "{0},{1},{2},{3}\n".format(size, sorted_insertions, mean, std)
      log( final_stat )
      f.write( final_stat )
      log ("=================================")