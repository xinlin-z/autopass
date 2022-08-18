#!/usr/bin/bash
dn=$(dirname $0)
cd $dn

passwd=$1
shift

while true; do
    python3 -u autopass.py $passwd $@
    sleep 8
done


