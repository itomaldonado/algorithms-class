import sys, timeit, argparse, time, random, json
from functools import partial

# For logging
LOG_ENABLED = False

class Graph:
  """
  Class implementing a Graph
  Graph: [
    vertex_1: [{v: b, w:12.3}, {v: c, w:12.3}, ..., {v:n, w:12.3}],
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
    self.__max_vertex = max_vertex
    self.__g = [[] for _ in range(self.__max_vertex) ]

    # setting the recursion limit to something higher than
    # what we may hit
    sys.setrecursionlimit(max_vertex + 10)

  def connect(self, a, b, w):
    """
    Connects vertex 'a' to vertex 'b'
    """
    if a < len(self.__g) or b < len(self.__g):
      # do the connection only when the vertices provided are in the graph
      self.__g[a].append({'v': b, 'w': w})

  def dijsktras(self, start=0):
    weights = [None for _ in range(self.__max_vertex)]
    visited = set([start])
    weights[start] = 0
    path = {}

    # Create set with list of nodes
    nodes = set([i for i in range(self.__max_vertex)])

    while nodes: 
      smallest_node = None
      for node in nodes:
        if node in visited:
          if smallest_node is None:
            smallest_node = node
          elif weights[node] < weights[smallest_node]:
            smallest_node = node

      if smallest_node is None:
        break

      nodes.remove(smallest_node)
      current_weight = weights[smallest_node]

      for edge in self.__g[smallest_node]:
        weight = current_weight + edge['w']
        if edge['v'] not in visited or weight < weights[edge['v']]:
          if edge['v'] not in visited: visited.add(edge['v'])
          weights[edge['v']] = weight
          path[str(edge['v'])] = smallest_node

    return visited, path

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
  start = time.clock()
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
      g.connect(int(ints[0]), int(ints[1]), float(ints[2])) # connect a and b
  log("Graph created Time: {0}".format( (time.clock() - start) ))

  # Finally, check if it has a cycle
  start = time.clock()
  visited, path = g.dijsktras(start=0)
  log("Dijsktra\'s calculated Time: {0}".format( (time.clock() - start) ))
  with open('./out.txt', 'wb') as f:
    f.write( json.dumps(path, indent=2) )
    print visited