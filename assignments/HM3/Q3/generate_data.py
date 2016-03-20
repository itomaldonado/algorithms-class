import sys
from random import shuffle

length = int(sys.argv[1])
int_list = [i for i in range(length)]
shuffle(int_list)
first = True
with open('./Data/data2.%s'%length, 'wb') as f:
  for item in int_list:
    if first:
      f.write("%s" % item)
      first = False
    else:
      f.write("\n%s" % item)