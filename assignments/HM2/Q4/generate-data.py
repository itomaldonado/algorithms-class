def generate_data():
  data = list()
  
  # Writte '1' 1024 times
  for i in xrange(0, 1024):
    data.append('1')

  # Write '11' 2048 times
  for i in xrange(0, 2048):
    data.append('11')

  # Write '111' 4096 times
  for i in xrange(0, 4096):
    data.append('111')

  # Write '1111' 1024 times
  for i in xrange(0, 1024):
    data.append('1111')

  return data


if __name__ == '__main__':
  data = 0
  data = generate_data()

  # Print out the results to q4.txt
  with open('./q4.txt', 'wb') as f:
    first = True
    for item in data:
      if first:
        f.write("%s" % item)
        first = False
      else:
        f.write("\n%s" % item)