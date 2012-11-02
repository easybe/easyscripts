#!/bin/sh

# easyb 2011

if [ $# -lt 2 ]; then
    echo "usage: `basename $0` OLD NEW [-s|-w]"
    exit
fi

old=$1
shift
new=$1
shift
echo "$@" | grep -q "\-s"
[ $? -eq 0 ] && sim="true"
echo "$@" | grep -q "\-w"
[ $? -eq 0 ] && word="true"

files=$(find . -type f \( ! -regex '.*/\..*' \) | \
    xargs grep $([ $word ] && echo "-w") -I -l \
    --exclude={*#*,*.*} --exclude-dir=.* $old 2>/dev/null)

for f in $files; do
    [ "$sim" ] && SIM="[SIM] "
    echo "${SIM}processing: $f"

    if [ -z "$sim" ]; then
        mode=$(stat -c"%a" $f)
        if [ "$word" ]; then
            oldRE='\b'$old'\b'
            newRE="$new"
        else
            oldRE="$new"
            newRE="$old"
        fi
        sed "s:$oldRE:$newRE:g" "$f" >"$f.tmp" && \
            mv "$f.tmp" "$f"
        chmod $mode $f
    fi
done
