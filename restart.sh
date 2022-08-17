#!/usr/bin/bash
dn=$(dirname $0)
cd $dn

passwd=$1
shift
cmd=$@

while true; do
    python3 autopass.py $passwd $cmd
    sleep 8
done


