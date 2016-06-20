import sys, timeit, argparse, time, random
from functools import partial

# For logging
LOG_ENABLED = False

class Graph:
  """
  Class implementing a Graph
  Graph: [
    vertex_1: [adj_vertex_1, adj_node_2, ..., adj_vertex_n],
    vertex_2: ...,
    ...
    vertex_n: ...
  ]
  """

  def __init__(self, max_vertex=10):
    """
    Initialize the Graph class
    """
    # Initialize the graph array representation with an empty array per vertex
    # If max_vertex is 10, we will have a graph with 10 vertices --> [0, 1, ..., 8, 9]
    self.__g = [[] for i in range(max_vertex)]

    # setting the recursion limit to something higher than
    # what we may hit
    sys.setrecursionlimit(max_vertex + 10)

  def connect(self, a, b):
    """
    Connects vertex 'a' to vertex 'b'
    """
    if a < len(self.__g) or b < len(self.__g):
      # do the connection only when the vertices provided are in the graph
      self.__g[a].append(b)

  def cycle(self):
    """
    Check if there is a cycle on the graph by doing DFS
    """
    # create a set of vertices to marke a visited vertex
    marked = set()
    path = set()
    return any(self.__dfs_cycle(vertex=i, marked=marked, path=path) for i in range(len(self.__g)))

  def print_graph(self):
    """
    Print the underlying data structure of the graph
    """
    for i in range(len(self.__g)):
      print("{0}: {1}".format(i, self.__g[i]))

  def __dfs_cycle(self, vertex=0, marked=set(), path=set()):
    """
    Private implementation for cycle seraching.
    Uses DFS and will stop when it reaches a marked node, return true for cycle.
    """
    log("Visiting: {0}".format(vertex))
    if vertex in marked:
      return False
    marked.add(vertex)
    path.add(vertex)
    log("Going to visit: {0}".format(self.__g[vertex]))
    for neighbour in self.__g[vertex]:
      if (neighbour in path) or (self.__dfs_cycle(vertex=neighbour, marked=marked, path=path)):
        log("Foind neighbor {0} in path, returning True for Cycle".format(neighbour))
        return True
    log("Done with vertex {0}, removing from path.".format(vertex))
    path.remove(vertex)
    return False

  def __str__(self):
    string = ''
    for v in range(len(self.__g)):
      string += "{0}: {1}\n".format(v, self.__g[v])
    return string

  def __repr__(self):
      return self.__str__()

# Logging Helper function
def log(txt):
  if LOG_ENABLED:
    print(txt)

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Cycle finding implementation')
  parser.add_argument('-l', '--log', help='Print trial stats', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()
  LOG_ENABLED = args.log

  max_vertex_found = False
  edges_found = False
  edges = 0
  g = None
  with open(args.file) as f:
   for line in f: # for each line
    line = line.rstrip('\n').rstrip('\r') # remove any new lines...
    
    if max_vertex_found is False: # first we get the max number of vertices
      g = Graph(max_vertex=int(line))
      max_vertex_found = True

    if edges_found is False: # second we get the number of edges
      edges =int(line)
      edges_found = True

    # finally we connect each edge
    ints = line.split(' ') # split the number pair into a, b and weight
    if len(ints) > 1:
      g.connect(int(ints[0]), int(ints[1])) # connect a and b

  # Finally, check if it has a cycle
  if g:
    with open('./out.txt', 'wb') as f:
      f.write( str(g) )
    print("Has cycle? --> {0}".format(g.cycle()))
  else:
    print("Could not create Graph object.")

