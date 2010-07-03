import os.path
from fabric.api import *

import config

env.hosts = [config.SSH_HOST]  # format: username@host:port

VIRTUALENV_DIR = '/home/igor/eizzek_env'
EIZZEK_DIR = os.path.join(VIRTUALENV_DIR, 'eizzek')

python = os.path.join(VIRTUALENV_DIR, 'bin', 'python')
twistd = os.path.join(VIRTUALENV_DIR, 'bin', 'twistd')


def update_deps(*deps):
    for dep in deps:
        print ' - Updating %s' % dep
        with cd( os.path.join(VIRTUALENV_DIR, dep) ):
            run('git pull')
            run('%s setup.py install' % python)


def update(all=False):
    ''' Update the project. Use :all to update all git depedencies '''
    if all:
        update_deps('wokkel')
    with cd(EIZZEK_DIR):
        print ' - Updating eizzek'
        run('git pull')
    send_config()


def start():
    ''' Start bot service '''
    with cd(EIZZEK_DIR):
        out = run('%s -y twistd.tac' % twistd)


def stop(force=False):
    ''' Stop the bot. Use :force to kill -9. Default is -15 ''' 
    with cd(EIZZEK_DIR):
        if 'twistd.pid' not in run('ls'):
            print ' - Not running'
            return
        pid = run('cat twistd.pid')
        force = '-9' if force else '-15'
        run( 'kill %s %s' % (force, pid) )


def send_config():
    ''' Send the local config.py to the server '''
    put('config.py', os.path.join(EIZZEK_DIR, 'config.py'))

