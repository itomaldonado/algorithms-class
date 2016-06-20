import sys, timeit, argparse, time, random, heapq
from functools import partial

# For logging
LOG_ENABLED = False

# Logging Helper function
def log(txt):
  if LOG_ENABLED:
    print(txt)

def bfs(max_vertex, graph=[], start=0):
  """
  BFS implementation
  """
  VISITED = set()
  QUEUE = [start]
  ORDER = list()
    
  while QUEUE: # empty stack
    v = QUEUE.pop(0)
    if v not in VISITED:
      VISITED.add(v)
      ORDER.append(v)
      QUEUE.extend(graph[v] - VISITED)
  return ORDER

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='BFS implementation')
  parser.add_argument('-l', '--log', help='Print trial stats', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()
  LOG_ENABLED = args.log

  max_vertex_found = False
  edges_found = False
  edge_count = 0
  max_vertex=0
  graph = None
  start = time.clock()
  with open(args.file) as f:
    for line in f: # for each line
      line = line.rstrip('\n').rstrip('\r') # remove any new lines...
      
      if max_vertex_found is False: # first we get the max number of vertices
        max_vertex = int(line)
        graph = [set() for i in range(max_vertex)]
        max_vertex_found = True

      if edges_found is False: # second we get the number of edges
        edge_count = int(line)
        edges_found = True

      # finally we connect each edge
      ints = line.split(' ') # split the number pair into a, b and weight
      if len(ints) > 1:
        graph[int(ints[0])].add(int(ints[1])) # connect a and b
  log("Graph created Time: {0}".format( (time.clock() - start) ))

  # Finally, get DFS
  start = time.clock()
  BFS = bfs(max_vertex=max_vertex, graph=graph, start=0)
  log("BFS calculated Time: {0}".format( (time.clock() - start) ))

  with open('./out.txt', 'wb') as f:
    # print the edges of the DFS
    for v in BFS:
      f.write( "{0}\n".format(str(v)) )
