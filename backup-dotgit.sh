#!/bin/sh

SRC=/local-home
DEST=/tmp/bu

old=$(ls -1 $DEST | tail -n 1)
new=$(date +"%Y-%m-%dT%H:%M:%S")

mkdir -p $DEST/$new

find $SRC -type d -name ".git" -print0 2>/dev/null | \
    rsync -arv --link-dest=$DEST/$old --files-from=- --from0 \
    / $DEST/$new
