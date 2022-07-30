# autopass

Enter password automatically for sudo, ssh and scp, like sshpass.

This is a pure python version which can help you input password for sudo,
ssh, scp and getpass of python. For ssh, a `yes` confirmation is also
issued automatically for you if needed.

**No any third party module is needed! No need pexpect!**

Usage Examples:

``` shell
$ python3 autopass.py -h
$ python3 autopass.py -V
$ python3 autopass.py 'passwd' sudo <command>
$ python3 autopass.py [-t30] 'passwd' ssh username@domain [-p port] <command>
$ python3 autopass.py 'passwd' scp [-P port] <file> username@domain:path
```

`-tN`, to specify a timeout in second. SIGKILL will be sent to child process
after timeout. No timeout by default.

Password will be issued only once, so if password is not correct,
the child process will wait for a long time. This is your chance to
place a timeout. Other cases might be caused by terrible network.

No any interactive is supported, autopass is focused on command execution
which need a password from tty (controlling terminal).

Exit code of command is return by autopass, so you can use `echo $?` in
your shell script to check if the command execution is successful.

Have fun...^____^
