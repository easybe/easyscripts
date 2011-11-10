#!/bin/sh

# easyb 2011

if [ $# -lt 3 ]; then
    echo "usage: `basename $0` OLD NEW [-d]"
    exit
fi

OLD=$1
NEW=$2
OPT=$3

grep -r -l --exclude-dir=.svn $OLD * |
    while read FILE
    do
        echo "processing: $FILE"

        if [ "x$OPT" == "x" ]; then
            sed "s/$OLD/$NEW/i;" "$FILE" >"$FILE.tmp"
            mv "$FILE.tmp" "$FILE"
        fi
    done