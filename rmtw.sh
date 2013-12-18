#!/bin/sh
test $# -lt 1 && exit 1
sed -i.back -e 's/[[:space:]]*$//g' -e ':a /^\n*$/{$d;N;ba}' $@
echo "done"
