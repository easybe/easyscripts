#!/bin/sh

if [ $(id -u) -ne 0 ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

[ "x$1" == "x-r" ] && restore=1 || restore=0

HOST="Easys-iPhone.local"
SRC="root@$HOST:/"
DST="/Volumes/Users/easyb/Documents/iPhone/bu"
FILES=$(cat <<EOF
/tmp/packages
/private/etc/apt
/private/etc/netatalk/AppleVolumes.default
EOF)

if [ $restore -ne 1 ]; then
    ssh root@$HOST "dpkg-query --show --showformat='\${Package}\\n' >/tmp/packages"

    echo "$FILES" | rsync -arzv --delete --files-from=- -e ssh $SRC $DST
else
    echo "$FILES" | rsync -arzvK --files-from=- $DST -e ssh $SRC

    ssh root@$HOST "apt-get update"
    ssh root@$HOST "apt-get install \$(cat /tmp/packages)"
fi
