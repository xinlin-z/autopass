* [Autopass](#Autopass)
    * [Usage Examples](#Usage-Examples)
* [repeat.sh](#repeatsh)

# Autopass

Enter password automatically for sudo, ssh(remote command) and scp,
like sshpass.

This is a pure python version which can help you input password for sudo,
ssh, scp. For ssh, a `yes` confirmation is also issued automatically
for you if necessary.

**No third party module is needed! No need pexpect!**

> The password-input-matching-pattern is fixed and dedicated for sudo,
ssh and scp in source code.

## Usage Examples

``` shell
$ python autopass.py -h
$ python autopass.py -V
$ python autopass.py -p'passwd' sudo <command>
$ python autopass.py [-t300] -p'passwd' ssh username@domain [-p port] <command>
$ python autopass.py -p'passwd' scp [-P port] <file> username@domain:path
```

You can also export password to `AUTOPASS` environment variable, this
can significantly reduce the exposure of password itself,
improve security. Like:

``` shell
$ export AUTOPASS=password
$ python autopass.py [-t300] ssh -l username domain.com [-p port] <command>
```

`-tN`, to specify a timeout in seconds. SIGKILL will be issued to
child process when timeout. No timeout by default.

`stdin redirection` is also supported:

``` shell
$ export AUTOPASS=password
$ python autopass.py ssh name@domain [-p port] 'bash -s' < script.sh
$ python autopass.py sudo <command> < input
```

And password can also be redirected into stdin:

```shell
$ echo -n 'abcd1234' | python3 autopass.py sudo <command>
$ python autopass.py sudo <command> <<< 'abcd1234'
```

Password will be issued only once, so if the password is not correct,
the child process will wait for a long time. This is your chance to
place a timeout. Other cases for using timeout might be the terrible network.
You can always place a relatively large timeout value to keep you from
waiting like forever.

Autopass is focused on command execution, locally or remotely. It cannot
be used interactively. And please do not start a background process by
autopass, like `-f` option of ssh. It is an error. But you definitely
could run autopass with command as a whole in background (use `&`).

Exit code of command is return by autopass, so you can use `echo $?` in
your shell script to check if the command execution is successful.

# repeat.sh

This is a very tiny shell script which can `repeat` your
whatever-command forever automatically! When use it with autopass,
it would be more powerful!

Usage Examples:

``` shell
$ export AUTOPASS=password
$ bash repeat.sh python autopass.py sudo <command>
$ bash repeat.sh python autopass.py <ssh command> >> log 2>&1 &
```

`stdin redirection` is supported by simple quoting the whole command:

``` shell
$ export AUTOPASS=password
$ bash repeat.sh 'python autopass.py sudo <command> | <command>'
$ bash repeat.sh 'python autopass.py <ssh command> bash -s < script.sh'
```

Please do not start a background process by repeat.sh,
like the `-f` option of ssh. It will cause autopass exit immediately.
But you definitely could run repeat.sh in background.

Have fun...^____^

