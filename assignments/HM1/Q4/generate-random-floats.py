import random, sys, argparse


if __name__ == '__main__':

  # Instantiate argument parser
  parser = argparse.ArgumentParser(description='Generate a list of floats between -10,000 and 10,000')
  parser.add_argument('count', help='count of floats to generate', type=int, default=8)

  # Get/parse arguments
  args = parser.parse_args()

  i = 0
  while (i < args.count):
    print str(random.uniform(-10000.00, 10000.00))
    i = i + 1
