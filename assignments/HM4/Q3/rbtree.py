import sys, timeit, argparse, time, random
from functools import partial

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
  Class implementing a RBT
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

  def contains(self, key):
    if key == None:
      raise Exception("argument to contains() is null")
    return self.get(key) != None

  def get(self, key):
    """
    Get the value associated with a given key starting at the given node
    Return 'None' if key does not exist
    """
    return self.__get(self.root, key)

  def __get(self, node, key):
    """
    Get the value associated with a given key
    If Node is 'None' return 'None'
    If key is smaller than node, search left subtree
    If key is larger than node, search right subtree
    If key is the same as node, return node value
    """
    if node == None:
      return None
    elif key < node['key']:
      return self.__get(node['left'], key)
    elif key > node['key']:
      return self.__get(node['right'], key)
    else:
      return node['val']

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
      return new_node(key=key, val=val, N=1, color=RED)
    elif key < node['key']:
      node['left'] = self.__put(node['left'], key, val)
    elif key > node['key']:
      node['right'] = self.__put(node['right'], key, val)
    else:
        node['val'] == val

    # Perform re-balancing operations
    if self.__red(node['right']) and not self.__red(node['left']):
      node = self.__rotate_left(node)

    if self.__red(node['left']) and self.__red(node['left']['left']):
      node = self.__rotate_right(node)

    if self.__red(node['left']) and self.__red(node['right']):
      self.__flip_colors(node)

    node['N'] = 1 + self.__size(node['left']) + self.__size(node['right'])
    return node

  def min(self):
    """
    Find the min value in the RBT and return the key
    return 'None' if RBT is empty
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
    Find the max value in the RBT and return the key
    return 'None' if RBT is empty
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
    Raise exception if position is less than zero or larger than RBT size
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

  def __rotate_right(self, node):
    """
    Making a left-leaning red link move to the right
    """
    left = node['left']
    node['left'] = left['right']
    left['right'] = node
    left['color'] = node['color']
    node['color'] = RED
    left['N'] = node['N']
    node['N'] = self.__size(node['left']) + self.__size(node['right']) + 1
    return left

  def __rotate_left(self, node):
    """
    Making a right-leaning red link move to the left
    """
    right = node['right']
    node['right'] = right['left']
    right['left'] = node
    right['color'] = node['color']
    node['color'] = RED
    right['N'] = node['N']
    node['N'] = self.__size(node['left']) + self.__size(node['right']) + 1
    return right

  def __flip_colors(self, node):
    """
    Flip the colors of a node and its children
    """
    node['color'] = RED
    node['left']['color'] = BLACK
    node['right']['color'] = BLACK

  def nodes(self):
    """
    Return a list of nodes doing an inorder traversal
    Should be O(n)
    """
    nodes = list()
    nodes = self.__nodes(nodes, self.root)
    return nodes

  def __nodes(self, node_list, node):
    """
    Private implementation of nodes
    Returns list of nodes starting at the 'node' parameter
    Adds them to the 'node_list'
    Does inorder traversal
    """
    if node is None:
      return node_list
    node_list = self.__nodes(node_list, node['left'])
    node_list.append(node)
    node_list = self.__nodes(node_list, node['right'])
    return node_list

  def get_red_links(self):
    """
    Return number of red links doing an inorder traversal
    Should be O(n)
    """
    links = 0
    links += self.__red_links(self.root)
    return links

  def __red_links(self, node):
    """
    Private implementation of get_red_links
    Returns number of red links
    Does inorder traversal
    """
    links = 0
    if node is None:
      return 0
    elif self.__red(node):
      links += 1
    links += self.__red_links(node['left'])
    links += self.__red_links(node['right'])
    return links

# Logging Helper function
def log(txt):
  if LOG_ENABLED:
    print(txt)

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Red-Black Tree implementation, list is randomly generated')
  parser.add_argument('-t', '--trials', help='number of trials', default=100)
  parser.add_argument('-l', '--log', help='Print trial stats', action='store_true', default=False)
  #parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()
  LOG_ENABLED = args.log
  trials = int(args.trials)
  sizes = [10000, 100000, 1000000]

  with open('./out.txt', 'wb') as f:
    f.write( "size,black_rate,rate_rate\n" )
    # For each size, run 100 trials
    # Prints average red/black percentages
    log ("=================================")
    for size in sizes:
      # Keep track of rates
      brate = list()
      rrate = list()
      for trial in range(1, trials+1):
        # Print trial number
        log("Size: {0}, Trial: {1}".format(size, trial))
        # Generate new random List
        start = time.clock()
        int_list = [i for i in range(size)]
        random.shuffle(int_list)
        log ( 'List Generation Time: {0}'.format( (time.clock() - start) ) )
        # Build tree
        start = time.clock()
        rbt = RBT()
        for i in range(0, len(int_list)):
          key = int_list[i]
          val = int_list[i]
          rbt.put(key,val)
        log ( 'RBT Generation Time: {0}'.format( (time.clock() - start) ) )
        # Get nodes
        start = time.clock()
        alinks = rbt.size()
        rlinks = rbt.get_red_links()
        blinks = alinks - rlinks
        log ( 'Red Link Count Time: {0}'.format( (time.clock() - start) ) )

        # Add rates to lists
        brate.append(float((float(blinks)/float(alinks))))
        rrate.append(float((float(rlinks)/float(alinks))))
        log ("---------------------------------")
      # Print average values for all trials
      b_avg_per = sum(brate) / float(len(brate))
      r_avg_per = sum(rrate) / float(len(rrate))
      # Print out the results to out.txt
      final_stat = "{0},{1},{2}\n".format(size, b_avg_per, r_avg_per)
      log( final_stat )
      f.write( final_stat )
      log ("=================================")