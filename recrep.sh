#!/bin/sh

# easyb 2011

usage () {
    echo "usage: $(basename $0) OLD NEW [-s|-w] [-f \"FILE(S)\"]"
}

if [ $# -lt 2 ]; then
    usage
    exit 1
fi

uname -s | grep -q NT && sedargs="-b"

old=$1
shift
new=$1
shift

files=""
while getopts ":hswf:" option; do
    case "$option" in
        f)  files="$OPTARG"
            ;;
        s)  sim="true"
            ;;
        w)  word="true"
            ;;
        h)  usage
            exit 0
            ;;
        :)  echo "Error: -$option requires an argument"
            usage
            exit 1
            ;;
        ?)  echo "Error: unknown option -$option"
            usage
            exit 1
            ;;
    esac
done

if [ -z "$files" ]; then
    files=$(find . -type f \( ! -regex '.*/\..*' \) \( ! -regex '.*/#.*' \) | \
        xargs grep $([ $word ] && echo "-w") -I -l $old 2>/dev/null)
fi

for f in $files; do
    [ "$sim" ] && SIM="[SIM] "
    echo "${SIM}processing: $f"

    if [ -z "$sim" ]; then
        if [ "$word" ]; then
            oldRE='\b'$old'\b'
            newRE="$new"
        else
            oldRE="$old"
            newRE="$new"
        fi
        sed -i.back $sedargs "s:$oldRE:$newRE:g" "$f" && rm "$f.back"
    fi
done
