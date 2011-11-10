#!/bin/sh

# easyb 2011

if [ $# -lt 2 ]; then
    echo "usage: `basename $0` OLD NEW [-s]"
    exit
fi

OLD=$1
NEW=$2
if [  "x$3" != "x"  ]; then
    OPT="[SIM] "
fi

grep -r -l --exclude-dir=.svn $OLD * |
    while read FILE
    do
        echo "${OPT}processing: $FILE"

        if [ "x$OPT" == "x" ]; then
            sed "s/$OLD/$NEW/i;" "$FILE" >"$FILE.tmp"
            mv "$FILE.tmp" "$FILE"
        fi
    done