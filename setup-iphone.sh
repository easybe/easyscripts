#!/bin/sh

HOST="Easys-iPhone.local"
KEY=$(cat ~/.ssh/id_rsa.pub)
CMDS=$(cat <<EOF
passwd
mkdir .ssh
echo $KEY > .ssh/authorized_keys
passwd mobile
mkdir /var/mobile/.ssh
echo $KEY > /var/mobile/.ssh/authorized_keys
chown -R mobile:mobile /var/mobile/.ssh
apt-get install rsync vim
ln -s vim /usr/bin/vi
EOF)

ssh root@$HOST "$CMDS"
