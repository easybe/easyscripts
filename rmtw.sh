#!/bin/sh
test $# -lt 1 && exit 1
sed -i.back -e 's/[[:space:]]*$//g' $@
echo "done"
