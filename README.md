# Autopass

* [Installation](#Installation)
* [Usage](#Usage)

Entering password automatically for sudo, ssh (remote command) and scp,
like sshpass. However, autopass is a pure Python version script.

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

**Password will be issued only once and only in the first line of output
for security reason**. So if the password is not correct,
the child process will wait for a long time. This is your chance to
set a timeout. Other cases such as a
terrible network, an unknown host or the fingerprint of host is not right,
etc, might also need a timeout to prevent from waiting too long.
You can always place a
relatively large timeout
value to keep you from waiting like forever.

Password can also be exported to `AUTOPASS` environment variable.

``` shell
$ export AUTOPASS='passwd'
$ python -m autopass <passwd-needed-command>
```

Autopass is a simple tool only for command execution, locally or remotely.
It cannot
be used interactively. And please do not start a background process by
autopass, like `-f` option of ssh. It is an error. But you definitely
could run autopass with command as a whole in background (by `&`).

Exit code of the executed command is returned properly, you can
use `echo $?` in your shell script to check if the command execution
is successful.

Have fun... ^____^

