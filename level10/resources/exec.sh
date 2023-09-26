#!/bin/bash

x=1

while [ $x -le 5000 ]
do
	../home/user/level10/level10 /tmp/1 0.0.0.0
	x=$(($x+1))
done
