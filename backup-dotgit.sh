#!/bin/sh

USER=buehler

[ -z "$SRC" ] && SRC=/local-home/$USER
[ -z "$DEST" ] && DEST=/netshares/hal/local-home/$USER/bu

old=$(ls -1 $DEST | tail -n 1)
new=$(date +"%Y-%m-%dT%H:%M:%S")

echo "Backing up to $DEST/$new ..."
echo "Taking $DEST/$old into account."

mkdir -p $DEST/$new

find $SRC -name ".git" -print0 2>/dev/null | \
    rsync -arv --link-dest=$DEST/$old --files-from=- --from0 \
    / $DEST/$new

new_files=$(find $DEST/$new -type f -links 1 | wc -l)
echo "Backed up $new_files new files"
echo
