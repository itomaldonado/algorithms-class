import sys, timeit, argparse, time, random, heapq
from functools import partial

# For logging
LOG_ENABLED = False

# Logging Helper function
def log(txt):
  if LOG_ENABLED:
    print(txt)

def prims(max_vertex, edges=[], start=0):
  """
  Prims implementation,
  uses an V by V matrix to store edge information

  edges --> [ [from, to, weight], [from, to, weight] ..... ]
  """
  graph = [[0]*max_vertex for _ in range(max_vertex) ]

  # Populating the graph
  for edge in edges:
    v_from, v_to, weight = edge[0], edge[1], edge[2]
    graph[v_from][v_to] = weight
    graph[v_to][v_from] = weight

  # create MST and VISITED
  MST = set()
  VISITED = set()

  VISITED.add(start) # add starting point
  while len(VISITED) != max_vertex:
    cross = set();
    # for each element a in VISITED, add the edge (a, b) to crossing if
    # b is not in VISITED
    for a in VISITED:
      for b in range(max_vertex):
        # if b isn't in visited and the wieght isn't 0
        if (b not in VISITED) and (graph[a][b] != 0) : 
          cross.add((a, b))
    
    # find the smallest weighting edge in the 'cross' set
    edge = sorted(cross, key=lambda e:graph[e[0]][e[1]])[0]

    # add this edge to MST
    MST.add(edge)

    # add the new vertex to VISITED
    VISITED.add(edge[1])

  return MST

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Prim\'s implementation')
  parser.add_argument('-l', '--log', help='Print trial stats', action='store_true', default=False)
  parser.add_argument('file', help='path to the file containing list of integers', default='')
  
  # Get/parse arguments
  args = parser.parse_args()
  LOG_ENABLED = args.log

  max_vertex_found = False
  edges_found = False
  edge_count = 0
  max_vertex=0
  edges = list()
  with open(args.file) as f:
   for line in f: # for each line
    line = line.rstrip('\n').rstrip('\r') # remove any new lines...
    
    if max_vertex_found is False: # first we get the max number of vertices
      max_vertex = int(line)
      max_vertex_found = True

    if edges_found is False: # second we get the number of edges
      edge_count = int(line)
      edges_found = True

    # finally we connect each edge
    ints = line.split(' ') # split the number pair into a, b and weight
    if len(ints) > 1:
      edges.append( [ int(ints[0]), int(ints[1]), float(ints[2])] ) # connect a and b and weight

  # Finally, get MST
  start = time.clock()
  MST = prims(max_vertex=max_vertex, edges=edges, start=0)
  log("MST Calculated Time: {0}".format( (time.clock() - start) ))

  with open('./out.txt', 'wb') as f:
    # print the edges of the MST
    for edge in MST:
      f.write( "{0}\n".format(str(edge)) )
