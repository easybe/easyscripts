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

find . -type f | xargs grep -I -l --exclude={#*,.*} --exclude-dir=.* $OLD 2>/dev/null |
    while read f; do
        echo "${OPT}processing: $f"

        if [ -z "$OPT" ]; then
            mode=$(stat -c"%a" $f)
            sed "s^$OLD^$NEW^g" "$f" >"$f.tmp" && \
            mv "$f.tmp" "$f"
            chmod $mode $f
        fi
    done
