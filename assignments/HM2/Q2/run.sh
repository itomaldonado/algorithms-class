#! /bin/bash

SIZES="1024 2048 4096 8192 16384 32768"

echo "Ordered"
for i in ${SIZES}; do
  python $1 ./Data/data0.$i
  head -1 ./out.txt
done

echo "Not Ordered"
for i in ${SIZES}; do
  python $1 ./Data/data1.$i
  head -1 ./out.txt
done