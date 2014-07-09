"""Filesytem module

Credit to Alexander Bulimov <lazywolf0@gmail.com>
for writing the Ansible module on which this is based."""

import sys
import os
import mcv.process

blkid_path = "/sbin/blkid"
mkfs_path = "/sbin/mkfs"

def partition(dev):
    """Partition a disk drive so it can get a filesystem
    set up on it; not fully supported yet."""
    pass

def mkfs(dev, dst_fstype, opts, force=False, verbose='error'):
    if not os.path.exists(dev):
        raise Exception("Device %s not found." % dev)

    cmd = [blkid_path, "-c", "/dev/null", "-o", "value", "-s", "TYPE", dev]
    print cmd
    out, err, status = mcv.process.execute(cmd, verbose=verbose)

    src_fstype = out.strip()

    if src_fstype == dst_fstype:
        return True

    elif src_fstype and not force:
        msg_tmpl = "{dev} is already used as {fs}, use force=True to overwrite"
        msg = msg_tmpl.format(dev=dev, fs=fs)
        sys.stderr.write(msg)
        return False

    else: # actually make the filesystem
        cmd = [mkfs_path, '-t', dst_fstype] + ([opts] if opts else []) + [dev]
        out, err, status = mcv.process.execute(cmd, verbose=verbose)
        if status != 0:
            sys.stderr.write("Creating filesystem %s on device '%s' failed" % (fstype,dev))
            return False
        return True
