# USAGE: fab --host=localhost catalog
# When prompted for postgres role passowrd, use 'passw0rd' for default config.
#
# Install the prerequisites:
#     apt-get install python-pip
#     pip install fabric
#
# Get the script, don't check out the entire repo (fabric will get the repo):
#     wget https://raw.github.com/azavea/Open-Data-Catalog/master/fabfile.py


from fabric import api as fab


# NOTE(xtoddx): I'm not well versed in Postgres, but making this be the
#               unix account name makes things simple, it seems.  Using
#               'catalog' for both a unix user and a postgres user is
#               recommended, as the sample config supports it.
DB_USER='catalog'

GIT_REPO='https://github.com/azavea/Open-Data-Catalog.git'


def apt_dependencies():
    fab.sudo('apt-get install --yes sendmail postgresql python-pip libpq-dev '
             'python-dev git')


def python_dependencies():
    fab.sudo('pip install virtualenv')


def dependencies():
    apt_dependencies()
    python_dependencies()


def virtualenv():
    fab.run('virtualenv opendatacatalog')


def source():
    with fab.cd('opendatacatalog'):
        fab.run('rm -rf Open-Data-Catalog || true')
        fab.run('git clone %s' % (GIT_REPO,))


def pip_from_app():
    with fab.cd('opendatacatalog/Open-Data-Catalog'):
        fab.run('PIP_DOWNLOAD_CACHE=../pip-cache ../bin/pip install -r '
                'requirements.txt')


def links_and_permissions():
    with fab.cd('opendatacatalog/Open-Data-Catalog/OpenDataCatalog'):
        fab.run('mkdir media')
        fab.run('chmod 755 media')
        fab.run('ln -s ../../lib/python2.7/site-packages/django/contrib/admin'
                'admin_media')


def create_postgres_user():
    fab.sudo('createuser -S -d -R -P %s' % (DB_USER,), user='postgres')

def create_postgres_table():
    fab.sudo('psql template1 -c '
             '"CREATE DATABASE catalog OWNER \\\\"%s\\\\";"' % (DB_USER,),
             user='postgres')

def postgres():
    create_postgres_user()
    create_postgres_table()


def syncdb():
    with fab.cd('opendatacatalog/Open-Data-Catalog/OpenDataCatalog'):
        fab.run('../../bin/python manage.py syncdb')


def catalog():
    dependencies()
    virtualenv()
    source()
    pip_from_app()
    links_and_permissions()
    postgres()
    syncdb()
