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

grep -r -I -l --exclude={#*,.*} --exclude-dir=.* $OLD * 2>/dev/null |
    while read FILE
    do
        echo "${OPT}processing: $FILE"

        if [ "x$OPT" == "x" ]; then
            sed "s/$OLD/$NEW/g ;" "$FILE" >"$FILE.tmp"
            mv "$FILE.tmp" "$FILE"
        fi
    done