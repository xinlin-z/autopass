# autopass

Input password automatically for sudo, ssh(remote command) and scp,
like sshpass.

This is a pure python version which can help you input password for sudo,
ssh, scp. For ssh, a `yes` confirmation is also
issued automatically for you if needed.

**No third party module is needed! No need pexpect!**

> The password-input-matching-pattern is fixed and dedicated for sudo,
ssh and scp in source code.

Usage Examples:

``` shell
$ python3 autopass.py -h
$ python3 autopass.py -V
$ python3 autopass.py 'passwd' sudo <command>
$ python3 autopass.py [-t30] 'passwd' ssh username@domain [-p port] <command>
$ python3 autopass.py 'passwd' scp [-P port] <file> username@domain:path
```

`-tN`, to specify a timeout in seconds. SIGKILL will be issued to
child process when timeout. No timeout by default.

Stdin redirection is also supported:

``` shell
$ python3 autopass.py 'passwd' ssh name@domain [-p port] 'bash -s' < script.sh
$ python3 autopass.py 'passwd' sudo <command> < input
$ echo 'abcd1234' | python3 autopass.py 'passwd' sudo <command>
```

Password will be issued only once, so if the password is not correct,
the child process will wait for a long time. This is your chance to
place a timeout. Other cases for using timeout might be the terrible network.
You can always place a relatively large timeout value to keep you from
waiting like forever.

Autopass is focused on command execution, locally or remotely. It cannot
be used interactively.

Exit code of command is return by autopass, so you can use `echo $?` in
your shell script to check if the command execution is successful.

## restart.sh

This is a very tiny shell script which can `restart` your
passwd-needed-command forever automatically!

Usage Examples:

``` shell
$ bash restart.sh 'passwd' <command>
$ bash restart.sh 'passwd' <command> >> log 2>&1 &
```

Have fun...^____^
