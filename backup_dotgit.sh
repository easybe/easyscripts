#!/bin/sh

SRC=/local-home
DEST= ...

old=$(ls -1 $DEST | tail -n 1)
new=$(date +"%Y-%m-%dT%H:%M:%S")

mkdir -p $DEST/$new

find $SRC -type d \( -name ".git" -o -name ".git_externals" \) -print0 | \
    rsync -pavr --delete --link-dest=$DEST/$old --files-from=- --from0 \
    / $DEST/$new
