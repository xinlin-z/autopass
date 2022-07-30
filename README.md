# autopass

Enter password automatically for sudo, ssh and scp, like sshpass.

This is a pure python version which can help you input password for sudo,
ssh, scp and getpass of python.

**No any third party module is needed!**

Usage Examples:

``` shell
$ python3 autopass.py -h
$ python3 autopass.py -V
$ python3 autopass.py 'passwd' sudo <command>
$ python3 autopass.py [-t30] 'passwd' ssh username@domain [-p port] <command>
$ python3 autopass.py 'passwd' scp [-P port] <file> username@domain:path
```

`-tN`, to specify a timeout in second. SIGKILL will be sent to child process
after timeout.

No any interactive is supported, autopass is focused to command execution
which need a password from tty.

Exit code of command is return by autopass, so you can use `echo $?` in
your shell script to check if the command execution is success.

