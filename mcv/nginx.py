import subprocess
from jinja2 import Template


def nginx_reload():
    return subprocess.call(["nginx -s reload"], shell=True)


def rollout_servers(template_path, config_path, addrs):
    """Render a set of server addresses into a template,
    copy the output into the configuration path and reload
    running nginx configuration

    Template must expect `addrs` variable"""
    tmpl = Template(open(template_path, "r").read())
    with open(config_path, "w") as f:
        f.write(tmpl.render(addrs=addrs))
    nginx_reload()

