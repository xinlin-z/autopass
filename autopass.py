#!/usr/bin/env python3
"""
Enter password automatically for sudo, ssh, scp.
No interactive process supported!

Author:    xinlin-z
Github:    https://github.com/xinlin-z/autopass
Blog:      https://cs.pynote.net
License:   MIT
"""
import sys
import os
import pty
import fcntl
import threading
import re
import argparse
import signal


OS_READ_CHUNK = 512


def _comm(fd, passwd):
    passed = False
    out = b''
    pos = 0
    while True:
        try:
            if passed:
                print(os.read(fd,OS_READ_CHUNK).decode(),end='',flush=True)
                continue
            out += os.read(fd, OS_READ_CHUNK)
        except OSError:
            break

        print(out[pos:].decode(), end='', flush=True)
        pos = len(out)
        # pattern for ssh and sudo
        if (b'Are you sure you want to continue'
                b' connecting (yes/no/[fingerprint])?' in out):
            os.write(fd, b'yes\n')
            out = b''
            pos = 0
        elif re.search(rb'[Pp]assword.*?:', out):
            os.write(fd, (passwd+'\n').encode())
            passed = True
        # only check first OS_READ_CHUNK bytes
        elif pos > OS_READ_CHUNK:
            passed = True


def _write_stdin(swp):
    stdin = sys.stdin.fileno()
    wf = open(swp, 'wb')  # buffered binary IO
    while out:=os.read(stdin,OS_READ_CHUNK):
        wf.write(out)
    wf.flush()  # flush at last
    wf.close()  # closefd=True is the default in open call


def _timeout_kill(pid):
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass


_VER = 'autopass V0.13 by xinlin-z'\
       ' (https://github.com/xinlin-z/autopass)'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=_VER)
    parser.add_argument('-t', type=int, metavar='seconds',
                help='timeout for issuing SIGKILL')
    parser.add_argument('-p', metavar='password',
                help='the password string used by autopass')

    # Command line's special components will neither be included
    # in sys.argv list, and nor for args.cmd list defined below.
    # They are all shell's, such as >, >>, <, <<, <<<, |, # comments,
    # and they are all supported!
    parser.add_argument('cmd', nargs=argparse.REMAINDER,
                help='the command to be executed')
    args = parser.parse_args()

    # check stdin if need to create another pipe
    isatty = sys.stdin.isatty()
    if not isatty:
        srp, swp = os.pipe()

    # Please single-quote the password when input manually!!
    # It's too easy to fail because of the special characters shell knows.
    # Pay attention to character $, it must be escaped, like \$, when
    # you use double-quote!
    if args.p is None:
        try:
            args.p = os.environ['AUTOPASS'].strip()
        except KeyError:
            print('* [autopass] no password found')
            sys.exit(1)

    # pipe & pty.fork
    rp, wp = os.pipe()
    pid, fd = pty.fork()
    if pid == 0:  # child
        os.close(rp)
        fcntl.fcntl(wp, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        try:
            if not isatty:
                os.dup2(srp, sys.stdin.fileno())
                os.close(srp)
                os.close(swp)
            os.execlp(args.cmd[0], *args.cmd)
        except OSError as e:
            os.write(wp, repr(e).encode())
            os.close(wp)
            os._exit(1)

    # parent, must close(wp) first
    os.close(wp)
    with open(rp,'rb') as f:
        err = f.read()
    # not empty means error in child
    if err:
        os.close(fd)
        if not isatty:
            os.close(srp)
            os.close(swp)
        os.wait()
        print('* [autopass] os.execlp error:', err.decode())
        sys.exit(101)

    # check if need to write child's stdin
    if not isatty:
        threading.Thread(target=_write_stdin,args=(swp,),daemon=True).start()

    # check if need to start SIGKILL timer
    if args.t:
        timer = threading.Timer(args.t, _timeout_kill, (pid,))
        timer.start()

    # communicate with control terminal of child
    th = threading.Thread(target=_comm,
                          args=(fd,args.p.strip()),
                          daemon=True)
    th.start()
    th.join()
    timer.cancel()

    # fd will be closed when chid is gone!
    # exit code
    _, wstatus = os.wait()
    ec = os.waitstatus_to_exitcode(wstatus)
    # If command process catches signals and then exit normally,
    # it appears exit normally, os.WIFSIGNALED is False.
    if os.WIFSIGNALED(wstatus):
        print('\n* [autopass] child process was killed by %d' % ec)
        sys.exit(102)
    sys.exit(ec)


