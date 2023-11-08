# autopass

* [Installation](#Installation)
* [Usage](#Usage)

Entering password automatically for sudo, ssh (remote command) and scp,
like sshpass. Autopass is a pure python version.
For ssh, a `yes` confirmation is also issued automatically
for you if necessary.

**No third party module is needed! No need pexpect!**

## Installation

```shell
$ pip install autopass
```

## Usage

``` shell
$ python -m autopass -p'passwd' sudo <command>
$ AUTOPASS='passwd' python -m autopass [-t<N>] ssh user@domain [-p port] <command>
```

`-p<passwd>`, specify the password.

`-t<N>`, specify a timeout in seconds. SIGKILL will be issued to
child process after timeout. No timeout by default.

Password will be issued only once, so if the password is not correct,
the child process will wait for a long time. This is your chance to
place a timeout. Other cases for using timeout might be facing the
terrible network. You can always place a relatively large timeout
value to keep you from waiting like forever.

Password can also be exported to `AUTOPASS` environment variable.

``` shell
$ export AUTOPASS='passwd'
$ python -m autopass <passwd-needed-command>
```

Autopass is focused on command execution, locally or remotely. It cannot
be used interactively. And please do not start a background process by
autopass, like `-f` option of ssh. It is an error. But you definitely
could run autopass with command as a whole in background (by `&`).

Exit code of the executed command is return by autopass, you can
use `echo $?` in your shell script to check if the command execution
is successful.

