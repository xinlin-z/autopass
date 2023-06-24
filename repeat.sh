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
    echo '*' $(date)
    echo '*' $ "$*"
    bash -c "$*" &
    child_pid=$!
    wait $child_pid
    echo '*' $(date)
    echo '*' exit code: $?
    sleep 5
done

