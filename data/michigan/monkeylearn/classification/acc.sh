#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 neg_file pos_file"
	exit 1
fi

neg="$(echo $(wc -l "$1") | cut -d" " -f1)"
pos="$(echo $(wc -l "$2") | cut -d" " -f1)"
total=$((neg + pos))
neg=$(echo $(grep "/negative/" "$1" | wc -l))
pos=$(echo $(grep "/positive/" "$2" | wc -l))
acc=$(echo "scale=2; $((neg + pos))/$total" | bc -l)
echo "accuracy: $acc"

