#!/usr/bin/env python3
"""
Author: xinlin-z
Blog:   https://cs.pynote.net
Github: https://github.com/xinlin-z/autopass

Usage Examples:
$ python3 autopass.py -h
$ python3 autopass.py -V
$ python3 autopass.py 'passwd' sudo <command>
$ python3 autopass.py [-t30] 'passwd' ssh username@domain [-p port] <command>
$ python3 autopass.py 'passwd' scp [-P port] <file> username@domain:path
"""
import sys
import os
import pty
import fcntl
import threading
import re
import argparse
import signal


# os.read is low-level, which only read once and return,
# set this variable to 1 to test this app,
# set to 4096 for normal operation!
OS_READ_CHUNK = 4096


def _comm(fd, passwd):
    # Buffered binary IO can make sure that write the whole piece down
    # in one write call, but flush might be needed.
    wf = open(fd, 'wb')

    passed = False
    out = b''
    while True:
        try:
            out += os.read(fd, OS_READ_CHUNK)
        except OSError:
            # The underlying process has been exitsed.
            # When in the case of no password needed,
            # here is the chance to print all out.
            print(out.decode(), end='')
            break

        if passed:
            print(out.decode(), end='')
            out = b''
            continue

        if (b'Are you sure you want to continue'
                b' connecting (yes/no/[fingerprint])' in out):
            wf.write('yes\n'.encode())
            wf.flush()
            print(out.decode(), end='')
            out = b''
        elif re.search(rb'[Pp]assword', out):
            wf.write((passwd+'\n').encode())
            wf.flush()
            passed = True
            print(out.decode(), end='')
            out = b''


def _write_stdin(swp):
    fd = sys.stdin.fileno()
    wf = open(swp, 'wb')  # buffered binary IO
    while out:=os.read(fd, OS_READ_CHUNK):
        wf.write(out)
    wf.flush()  # flush at last
    wf.close()  # closefd=True is the default in open call


def _timeout_kill(pid, timeout):
    try:
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version',
                version='V0.10 by xinlin-z with love of Python')
    parser.add_argument('-t', type=int, metavar='seconds',
                help='SIGKILL will be sent after this seconds')
    parser.add_argument('passwd',
                help='the password which will be entered automatically')
    parser.add_argument('cmd', nargs=argparse.REMAINDER,
                help='the command line you want to executed')

    # Command line's special components will not be included
    # in sys.argv list, and so for args.cmd defined above.
    # They are all shell's, such as >, >>, <, <<, <<<, |, # comments,
    # and they are all supported!
    args = parser.parse_args()

    # check stdin if need to create another pipe
    isatty = sys.stdin.isatty()
    if not isatty:
        srp, swp = os.pipe()

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
    with open(rp, 'rb') as f:
        out = f.read()
    # not empty means error in child
    if len(out):
        print('####[autopass] execlp error:', out.decode())
        os.close(fd)
        if not isatty:
            os.close(srp)
            os.close(swp)
        os.wait()
        sys.exit(8)  # child invoke failed

    # check if to write child's stdin
    if not isatty:
        th = threading.Thread(target=_write_stdin, args=(swp,), daemon=True)
        th.start()

    # check if to start SIGKILL timer
    if args.t:
        tk = threading.Timer(args.t, _timeout_kill, (pid,args.t))
        tk.start()

    # communication with control terminal of child
    th = threading.Thread(target=_comm,
                          args=(fd,args.passwd.strip()), daemon=True)
    th.start()
    th.join()

    # try to close controlling terminal's fd, which always failed.
    try:
        os.close(fd)
    except OSError:
        pass

    # exit with command exit code
    _, wstatus = os.wait()
    if wstatus & 0x00FF != 0:
        print('\n####[autopass] kill by SIGKILL due to timeout')
        sys.exit(9)  # kill by SIGKILL
    sys.exit(os.waitstatus_to_exitcode(wstatus))


