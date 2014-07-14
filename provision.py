#!/usr/bin/env python

import labrador, labrador.cache.yaml_cache
import mcv.user, mcv.filesystem, mcv.file, mcv.git, mcv.apt, mcv.dir
import os
import shutil

lab = labrador.Labrador(cache=labrador.cache.yaml_cache.YamlCache('.labcache.yml'))

users = [['elliot', 'elliot42'],
         ['thomson', 'itsthomson'],
         ['jeff', 'kyptin']]

framed_attrs = { 'group': 'framed', 'mode': 02775 }

paths = mcv.dir.tree(
  ('/opt', [
      ('framed', framed_attrs, [
          ('archive'),
          ('deploy'),
          ('intake'),
          ('repo'),
          ('report')]),
      ('mcv', framed_attrs, [
          ('ssh')])]))

ssh_opts = { 'StrictHostKeyChecking': 'no' }

git_uri = 'git@github.com:framed-data/intake-mixpanel.git'
ssh_key = mcv.dir.subpath(paths, 'ssh', 'framed_deploy_id_rsa')

if __name__ == "__main__":
    # desired_rev = sys.argv[1]

    mcv.user.groupadd('framed')
    mcv.dir.mktree(paths)

    # mcv.filesystem.partition('/dev/sdb')
    # mcv.filesystem.mkfs('/dev/sdb1', 'ext3', {})
    # mcv.filesystem.set_mount({
    #     'src': '/dev/sdb1',
    #     'name': '/opt/framed',
    #     'fstype': 'ext3'
    # })
    # mcv.filesystem.mount('/opt/framed')


    for user, github in users:
        mcv.user.add(
            user,
            mod_opts={'groups': ['framed', 'sudo']},
            ext_opts={'authorized_keys':
                lab.g('https://github.com/{}.keys'.format(github))})
    mcv.user.userdel('max')

    repo_path = mcv.dir.subpath(paths, 'repo', 'intake-mixpanel')

    mcv.git.clone(
        git_uri,
        repo_path,
        ssh_key,
        ssh_opts=ssh_opts)

    mcv.git.fetch(
        repo_path,
        ssh_key,
        ssh_opts=ssh_opts)

    rev = mcv.git.current_rev(repo_path)

    mcv.git.export(
        repo_path,
        mcv.dir.subpath(paths, 'deploy', 'intake-mixpanel', rev),
        rev=rev,
        opts={'mode': 02775,
              'group': 'framed',
              'parents': True,
              'recursive': True})

    # deploy_path_latest = os.path.join(deploy_root, 'latest')
    # mcv.file.link(deploy_path_rev, deploy_path_latest)

    shutil.copy(
        os.path.join(, 'init', 'framed-intake-mixpanel.conf'),
        os.path.join('/etc/init', 'framed-intake-mixpanel.conf'))

    # restart the service
