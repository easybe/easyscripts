#!/bin/sh
# SPDX-License-Identifier: MIT
test $# -lt 1 && exit 1
sed -i.back -e 's/[[:space:]]*$//' -e ':a /^\n*$/{$d;N;ba}' $@
echo "done"
