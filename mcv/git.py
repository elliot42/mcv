import subprocess

# def clone(repo_uri, dest, bare=False):
#     subprocess
# 
# def fetch(repo_path
# 
def rev_parse(repo_path, rev='HEAD'):
    out = subprocess.check_output(['/usr/bin/git', 'rev-parse', rev])
    return out.strip()

def export_rev(repo_uri, rev=None):
    final_rev = rev if rev else head_rev(repo_uri)
