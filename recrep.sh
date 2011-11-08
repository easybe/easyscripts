#!/bin/sh

if [ $# -lt 3 ]; then
    echo "usage: `basename $0` 'file_regexp' old new [-d]"
    exit
fi

REGEXP="$1"
OLD=$2
NEW=$3
OPT=$4

find . -type f -name "$REGEXP" -print |
    while read FILE
    do
        #echo "processing $FILE:"

        FOUND=`grep "$OLD" $FILE`
        if [ "x$FOUND" != "x" ]; then
            echo "matches in $FILE"
        fi

        if [ "x$OPT" == "x" ]; then
            sed "s/$OLD/$NEW/i;" "$FILE" >"$FILE.tmp"
            mv "$FILE.tmp" "$FILE"
        fi
    done