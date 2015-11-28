import os
import sys

datadir = os.environ['OPENSHIFT_DATA_DIR']
ODOO_ROOT_DIR = os.path.join(datadir, 'odoo-repo')
if ODOO_ROOT_DIR not in sys.path:
    sys.path.append(ODOO_ROOT_DIR)

## GETTING-STARTED: make sure the next line has the right python version:
virtenv = os.environ['APPDIR'] + '/virtenv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.7/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except:
    pass


# WSGI Handler sample configuration file.
#
# Change the appropriate settings below, in order to provide the parameters
# that would normally be passed in the command-line.
# (at least conf['addons_path'])
#
# For generic wsgi handlers a global application is defined.
# For uwsgi this should work:
#   $ uwsgi_python --http :9090 --pythonpath . --wsgi-file openerp-wsgi.py
#
# For gunicorn additional globals need to be defined in the Gunicorn section.
# Then the following command should run:
#   $ gunicorn openerp:service.wsgi_server.application -c openerp-wsgi.py


import openerp
import uuid

#----------------------------------------------------------
# Common
#----------------------------------------------------------
openerp.multi_process = True # Nah!

# Equivalent of --load command-line option
conf = openerp.tools.config
openerp.conf.server_wide_modules = ['web']

# NEW CONF
conf['conf'] = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'odoo.conf')

# OLD CONF
#conf['conf'] = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'odoo.conf')
repodir = os.environ['OPENSHIFT_REPO_DIR']
addons_list= [
    os.path.join(datadir, 'odoo-repo', 'addons'),
    os.path.join(repodir, 'addons')]
conf['addons_path'] = ','.join(addons_list)
#conf['log_file'] = os.path.join(os.environ['OPENSHIFT_LOG_DIR'], 'odoo.log')
conf['data_dir'] = datadir
#conf['admin_passwd'] = os.environ.get('ODOO_ADMIN_PASSWD')
# Database config
#conf['db_name'] = os.environ['OPENSHIFT_APP_NAME']
conf['db_host'] = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
conf['db_user'] = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
conf['db_port'] = int(os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'])
conf['db_password'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']

#----------------------------------------------------------
# Generic WSGI handlers application
#----------------------------------------------------------
application = openerp.service.wsgi_server.application
openerp.service.server.load_server_wide_modules()

server = openerp.service.server.ThreadedServer(application)
server.cron_spawn()

#----------------------------------------------------------
# Gunicorn
#----------------------------------------------------------
# Standard OpenERP XML-RPC port is 8069
# bind = '127.0.0.1:8069'
# pidfile = '.gunicorn.pid'
# workers = 4
# timeout = 240
# max_requests = 2000


if __name__ == '__main__':
    # for local tests
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8069, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
