#!/usr/bin/bash
dn=$(dirname $0)
cd $dn


# The signals SIGKILL and SIGSTOP cannot be caught, blocked or ignored.
# So, we have no need to trap them here.
trap kill9 SIGINT SIGTERM SIGHUP EXIT
function kill9() {
    kill -9 $child_pid
    exit $?
}

while true; do
    echo ---- start at: $(date)
    bash -c "python3 -u autopass.py $*" &
    child_pid=$!
    wait $child_pid
    echo ---- exit code $?
    sleep 16
done

