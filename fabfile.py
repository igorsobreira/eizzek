from os.path import join
from fabric.api import *

import config

env.hosts = [config.SSH_HOST]  # format: username@host:port

VIRTUALENV_DIR = '/home/igor/eizzek_env'
EIZZEK_DIR = join(VIRTUALENV_DIR, 'eizzek')

python = join(VIRTUALENV_DIR, 'bin', 'python')


def update_sleekxmpp():
    with cd(join(VIRTUALENV_DIR, 'SleekXMPP')):
        run('git pull')
        run('%s setup.py install' % python)

def update():
    with cd(EIZZEK_DIR):
        run('git pull')
        send_config()


# def start():
#     with cd(EIZZEK_DIR):
#         out = run('screen -dm "%s main.py"' % python)
#         print out


def send_config():
    config = local('cat config.py')
    with cd(EIZZEK_DIR):
        run('echo "%s" > config.py' % config)

