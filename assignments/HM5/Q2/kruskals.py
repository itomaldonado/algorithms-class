import sys, timeit, argparse, time, random, heapq
from functools import partial

# For logging
LOG_ENABLED = False

# Logging Helper function
def log(txt):
  if LOG_ENABLED:
    print(txt)


def kruskals(max_vertex, __edges=[], start=0):
  """
  Kruskals implementation,
  uses an V by V matrix to store edge information

  edges --> [ [from, to, weight], [from, to, weight] ..... ]
  """
  # Populating the graph
  parent = list(i for i in range(max_vertex))
  rank = list( 0 for _ in range(max_vertex))

  # Convert edges to a list of sets
  edges = list()
  for edge in __edges:
    edges.append( (edge[0], edge[1], edge[2]) )

  MST = set()
  edges.sort()
  for edge in edges:
    a, b, weight = edge
    if find(parent, a) != find(parent, b):
      parent, rank = union(parent, rank, a, b)
      MST.add(edge)
  return MST

def find(parent, v):
  if parent[v] != v:
    parent[v] = find(parent, parent[v])
  return parent[v]

def union(parent, rank, a, b):
  root1 = find(parent, a)
  root2 = find(parent, b)
  if root1 != root2:
    if rank[root1] > rank[root2]:
      parent[root2] = root1
    else:
      parent[root1] = root2
      if rank[root1] == rank[root2]: rank[root2] += 1
  return parent, rank

if __name__ == '__main__':
  
  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Kruskal\'s implementation')
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
  MST = kruskals(max_vertex=max_vertex, __edges=edges, start=0)
  log("MST Calculated Time: {0}".format( (time.clock() - start) ))

  with open('./out.txt', 'wb') as f:
    # print the edges of the MST
    for edge in MST:
      f.write( "{0}\n".format(str(edge)) )
