
import subprocess
import shlex
import os


def run_cmd(cmd):
    assert isinstance(cmd, str)
    ret = subprocess.check_output(shlex.split(cmd))
    return ret.decode('utf-8')


def read_file(filename):
    assert isinstance(filename, str)
    assert os.path.exists(filename)
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content
