import sys, timeit, argparse, time, random
from functools import partial
from math import sqrt

###############
# Increasing the recursion limit since we will be doing recursive puts on a tree
sys.setrecursionlimit(10**6)
###############

# For logging
LOG_ENABLED = False

def new_node(key=None, val=None, left=None, right=None, N=0):
  """
  Create a new node structure
  """
  new_node = {
    'key': key,
    'val': val,
    'left': left,
    'right': right,
    'N': N
  }
  return new_node

class BST:
  """
  Class implementing a BST
  A node is a dict of:
  {
    'key' --> sorted by key
    'val' --> associated data
    'left' --> left subtree
    'right' --> right subtree
    'N' --> number of nodes in subtree
  }
  """

  def __init__(self):
    """
    Initialize the BST class
    """
    self.root = None

  def empty(self):
    """
    returns true if BST is of size 0
    """
    return self.size() == 0

  def size(self):
    """
    Returns the size of the BST
    """
    return self.__size(self.root)

  def __size(self, node):
    """
    Private method, returns size of a specific node
    """
    if node == None:
      return 0
    
    return node['N']

  def contains(self, key):
    if key == None:
      raise Exception("argument to contains() is null")
    return self.get(key) != None

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
    if node == None:
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
    Put the key,value in the BST
    Raise exception if key is None
    Delete key if value is None
    """
    if key == None:
      raise Exception("key is None")
    if val == None:
      self.delete(key)
      return None
    self.root = self.__put(self.root, key, val)

  def __put(self, node, key, val):
    """
    Private implementation of put.
    If node is None, create a new node with key, val of node count of 1
    If key is smaller than node, put the new node in the left subtree
    If key is larger than node, put the new node in the right subtree
    If keys equal, change the value of this node
    Finally, update the node's count
    """
    if node == None:
      return new_node(key=key, val=val, N=1);    
    elif key < node['key']:
      node['left'] = self.__put(node['left'], key, val)
    elif key > node['key']:
      node['right'] = self.__put(node['right'], key, val)
    else:
        node['val'] == val
    node['N'] = 1 + self.__size(node['left']) + self.__size(node['right'])
    return node

  def delete_min(self):
    """
    Delete the min value 
    Do nothing if BST is empty
    """
    if self.empty():
      return None
    else: 
      self.root = __delete_min(self.root)

  def __delete_min(self, node):
    """
    Private implementation of delete min.
    """
    if node['left'] == None:
      return node['right']
    node['left'] = self.__delete_min(node['left']);
    node['N'] = self.__size(node['left']) + self.__size(node['right']) + 1
    return node

  def delete_max(self):
    """
    Delete the max value 
    Do nothing if BST is empty
    """
    if self.empty():
      return None
    else: 
      self.root = __delete_max(self.root)

  def __delete_max(self, node):
    """
    Private implementation of delete max.
    """
    if node['right'] == None:
      return node['left']
    node['right'] = self.__delete_max(node['right']);
    node['N'] = self.__size(node['left']) + self.__size(node['right']) + 1
    return node

  def delete(self, key):
    """
    Delete a key
    Raise exception if key is None
    """
    if key == None:
      raise Exception("key is None")
    self.root = self.__delete(self.root, key)

  def __delete(self, node, key):
    """
    Private implementation of delete 
    """
    if node == None:
      return None
    elif key < node['key']:
      node['left'] = self.__delete(node['left'], key)
    elif key > node['key']:
      node['right'] = self.__delete(node['right'], key)
    else:
      if node['right'] == None:
        return node['left']
      if node['left'] == None:
        return node['right']
      temp = node
      node = self.__min(temp)
      node['right'] = self.__delete_min(temp['right'])
      node['left'] = temp['left']
    node['N'] = self.__size(node['left']) + self.__size(node['right']) + 1
    return node

  def min(self):
    """
    Find the min value in the BST and return the key
    return 'None' if BST is empty
    """
    if self.empty():
      return None
    else:
      min_node = self.__min(self.root)
      return min_node['key']

  def __min(self, node):
    """
    Private implementation of min
    """
    if node['left'] == None:
      return node
    else:
      return self.__min(node['left'])

  def max(self):
    """
    Find the max value in the BST and return the key
    return 'None' if BST is empty
    """
    if self.empty():
      return None
    else:
      max_node = self.__max(self.root)
      return max_node['key']

  def __max(self, node):
    """
    Private implementation of max
    """
    if node['right'] == None:
      return node
    else:
      return self.__max(node['right'])

  def floor(self, key):
    """
    Return the floor key for a given keyword
    Raises exception if key is None
    Returns None if tree is empty
    """
    if key == None:
      raise Exception("key is None")
    if self.empty():
      return None

    node = self.__floor(self.root, key)
    if node == None:
      return None
    else:
      return node['key']

  def __floor(self, node, key):
    """
    Private implementation of floor
    """
    if node == None:
      return None 
    elif key == node['key']:
      return node
    elif key < node['key']:
      return self.__floor(node['left'], key)

    temp = self.__floor(node['right'], key)
    if temp == None:
      return node
    else:
      return temp

  def ceiling(self, key):
    """
    Return the ceiling key for a given keyword
    Raises exception if key is None
    Returns None if tree is empty
    """
    if key == None:
      raise Exception("key is None")
    if self.empty():
      return None

    node = self.__ceiling(self.root, key)
    if node == None:
      return None
    else:
      return node['key']

  def __ceiling(self, node, key):
    """
    Private implementation of ceiling
    """
    if node == None:
      return None 
    elif key == node['key']:
      return node
    elif key > node['key']:
      return self.__ceiling(node['right'], key)

    temp = self.__ceiling(node['left'], key)
    if temp == None:
      return node
    else:
      return temp

  def select(self, pos):
    """
    Select a key in a given position
    Raise exception if position is less than zero or larger than BST size
    """
    if (pos < 0) or (pos >= self.size()):
      raise Exception('Position is out of bounds') 
    node = self.__select(self.root, pos)
    return node['key']

  def __select(self, node, pos):
    """
    Private implementation of select
    """
    if node == None:
      return None

    size_left = self.__size(node['left'])
    if size_left > pos:
      return self.__select(node['left'], pos)
    elif size_left < pos:
      return self.__select(node['right'], (pos - size_left - 1))
    else:
      return node

  def rank(self, key):
    """
    Return the rank of a given key
    Raise exception if key is None
    """
    if key == None:
      raise Exception("key is None")
    return self.__rank(self.root, key)

  def __rank(self, node, key):
    """
    Private implementation of rank
    """
    if node == None:
      return None
    elif key < node['key']:
      return self.__rank(node['left'], key)
    elif key > node['key']:
      return (1 + self.__size(node['left']) + self.__rank(node['right'], key))
    else:
      return self.__size(node['left'])


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
        bst = BST()
        for item in int_list:
          bst.put(item,item)
        log ( 'BST Generation Time: {0}'.format( (time.clock() - start) ) )
        # Get Path length to random element
        element = random.randrange(1, size+1) # get a random element key
        path_length = bst.path(element) # calculate path length
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