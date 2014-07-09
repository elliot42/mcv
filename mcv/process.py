"""Helper functions for executing processes locally;
generally thin wrappers around stdlib's `subprocess`"""

import sys
import subprocess
import StringIO
import itertools

sudo_path = "/usr/bin/sudo"

def execute(cmd_in, sudo=False, verbose='error'):
    if sudo:
        if isinstance(cmd_in, basestring):
            cmd = sudo_path + " " + cmd_in
        else:
            cmd = [sudo_path] + cmd_in
    else:
        cmd = cmd_in

    if verbose == True:
        sys.stderr.write(str(cmd))

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_it = itertools.imap(lambda x: ['stdout', x], iter(p.stdout.readline, ''))
    err_it = itertools.imap(lambda x: ['stderr', x], iter(p.stdout.readline, ''))
    combined_it = itertools.chain(out_it, err_it)
    streams = {
        'stdout': sys.stdout,
        'stderr': sys.stderr
    }

    output = {
        'stdout': [],
        'stderr': []
    }
    for stream, line in combined_it:
        output[stream] += line
        if verbose == True:
            streams[stream].write(line + "\n")
    p.communicate()
    status = p.returncode

    out = '\n'.join(output['stdout'])
    err = '\n'.join(output['stderr'])

    if not verbose and status != 0:
        for stream, lines in output.iteritems():
            output[stream].write('\n'.join(lines))

    if verbose == True or (verbose == 'error' and status != 0):
        sys.stderr.write("Exited with status {}".format(status))

    return [out, err, status]
