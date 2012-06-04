#!/bin/sh

if [ $# -lt 2 ]; then
    echo "usage: `basename $0` OLD_PREFIX NEW_PREFIX [-s]"
    exit
fi

old=$1
new=$2

[ "x" != "x$3" ] && SIM=echo

for f in *; do
    com=${f#$old}
    $SIM mv $f $new$com
done
