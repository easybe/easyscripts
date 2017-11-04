#!/bin/bash -e
host='localhost'
user='root'
read -p "Password: " -s pw

if [ $1 = "-i" ]; then
    for f in *; do
        db=${f%%.sql.gz}
        zcat $f | mysql -u $user --password=$pw $db
    done
else
    for db in $(mysql -h $host -u $user --password=$pw --batch --skip-column-names --execute="show databases"); do
        f=$db.sql.gz
        mysqldump $db -h $host -u $user --password=$pw --triggers --routines --single-transaction | gzip -c > $f
    done
fi
