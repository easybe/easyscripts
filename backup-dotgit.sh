#!/bin/sh

USER=buehler

SRC=/local-home/$USER
DEST=/netshares/hal/local-home/$USER/bu

old=$(ls -1 $DEST | tail -n 1)
new=$(date +"%Y-%m-%dT%H:%M:%S")

echo "Backing up to $DEST/$new ..."
mkdir -p $DEST/$new

find $SRC -type d -name ".git" -print0 2>/dev/null | \
    rsync -arv --link-dest=$DEST/$old --files-from=- --from0 \
    / $DEST/$new
