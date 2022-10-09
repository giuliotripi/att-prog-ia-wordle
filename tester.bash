#!/bin/bash

FAILED=0
OK=0

declare -A attempts

for i in $(seq 1000); do
  TIMES=$(python3 client.py en 5 | grep GUESSED)

  if [[ $? -eq 0 ]]; then
    OK=$((OK+1))
    TIMES=$(echo $TIMES | cut -f 4 -d" ")
    ((attempts[$TIMES]++))
#    echo $TIMES
  else
    FAILED=$((FAILED+1))
  fi
done;

echo "OK $OK, FAILED: $FAILED, $attempts"

for i in $(seq 6); do
  echo $i: "${attempts[$i]}"
done