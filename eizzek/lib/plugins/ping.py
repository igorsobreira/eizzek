import subprocess
from eizzek.lib.decorators import plugin


@plugin(r'^ping (?P<url>.+)$')
def ping(url):
    cmd = 'ping -c 3 %s' % url
    popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    out, _ = popen.communicate()
    return out
