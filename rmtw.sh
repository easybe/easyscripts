#!/bin/sh
test $# -lt 1 && exit 1
sed -i '.back' -E 's/[[:space:]]*$//g' $@
echo "done"
