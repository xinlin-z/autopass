#!/usr/bin/bash
dn=$(dirname $0)
cd $dn

passwd=$1
shift

# The signals SIGKILL and SIGSTOP cannot be caught, blocked or ignored.
# So, we have no need to tray them here.
trap kill9 SIGINT SIGTERM SIGHUP EXIT
function kill9() {
    kill -9 $child_pid
    exit $?
}

while true; do
    echo ---- $(date) ----
    python3 -u autopass.py $passwd $@ &
    child_pid=$!
    wait $child_pid
    sleep 16
done

