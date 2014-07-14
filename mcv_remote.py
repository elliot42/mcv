#!/usr/bin/env python

from __future__ import absolute_import

import mcv.remote, mcv.remote.apt, mcv.remote.pip
import sys
import os
from contextlib import contextmanager

hosts = ['dev04.corp.framed.io',
         'dev05.corp.framed.io',
         'dev06.corp.framed.io',
         'web01.corp.framed.io',
         'worker01.corp.framed.io']

deploy_root = "/opt/mcv"

@contextmanager
def status(msg, newline=False):
    sys.stderr.write(msg + ("\n" if newline else ": "))
    yield
    sys.stderr.write((msg + ": " if newline else "") + "Done.\n")

@contextmanager
def bootstrap(conn_spec, verbose='error'):
    with mcv.remote.connection(conn_spec, verbose=verbose) as ssh:
       with status("Bootstrap (apt)"):
           mcv.remote.apt.install(ssh, ['python-pip', 'python-dev', 'git'])

       with status("Bootstrap (pip)"):
           mcv.remote.pip.install(
               ssh,
               ['labrador'],
               upgrade=True,
               sudo=True)

       with status("Bootstrap (deploy)"):
           mcv.remote.deploy(
               ssh,
               '.',
               '/opt/mcv',
               excludes=['.git', '.vagrant', 'build', 'mcv.egg-info', 'dist', '*.vhd'],
               sudo=True)

       sys.stderr.write("Bootstrap complete.\n")

       yield ssh

if __name__ == "__main__":
    conn_specs = [dict(mcv.remote.conn_spec().items() +
                     {'host': 'localhost',
                      'port': 2222,
                      'username': 'vagrant',
                      'key_filename': '/home/elliot/.vagrant.d/insecure_private_key'
                      }.items())]

    for conn_spec in conn_specs:
        with bootstrap(conn_spec) as ssh:
            if len(sys.argv) < 2:
                sys.stderr.write("No args provided; exiting after bootstrap.\n")
            else:
                with status("Executing: {}".format(sys.argv[1]), newline=True):
                    out, err, exit_status = mcv.remote.execute(
                        ssh,
                        os.path.join(deploy_root, sys.argv[1]),
                        sudo=True)
                    sys.stdout.write(out)
                    sys.stderr.write(err)
