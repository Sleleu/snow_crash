#!/bin/bash

x=1

while [ $x -le 5000 ]
        do
        ln -sf /home/user/level10/token /tmp/1
	ln -sf /tmp/2 /tmp/1
        x=$(($x+1))
done
