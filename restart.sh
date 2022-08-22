#!/usr/bin/bash
dn=$(dirname $0)
cd $dn

passwd=$1
shift

trap 'kill9' SIGINT SIGTERM SIGKILL SIGHUP EXIT
function kill9() {
    kill -9 $child_pid
    exit $?
}

while true; do
    echo ---- $(date) ----
    python3 -u autopass.py $passwd $@ &
    child_pid=$!
    wait $child_pid
    sleep 8
done


