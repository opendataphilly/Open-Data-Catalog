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
GIT_REPO='https://github.com/openlexington/Open-Data-Catalog.git'
OVERLAY_REPO='https://github.com/openlexington/ODC-overlay.git'


def unix_user():
    fab.sudo('useradd -m -G sudo %s' % (DB_USER,))

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
                '/admin_media')


def create_postgres_user():
    fab.sudo('createuser -S -d -R -P %s' % (DB_USER,), user='postgres')


def create_postgres_table():
    fab.sudo('psql template1 -c '
             '"CREATE DATABASE catalog OWNER \\\\"%s\\\\";"' % (DB_USER,),
             user='postgres')


def postgres():
    create_postgres_user()
    create_postgres_table()


def local_settings():
    with fab.cd('opendatacatalog/Open-Data-Catalog/OpenDataCatalog'):
        fab.run('cp local_settings.py.example local_settings.py')


def style_overlay():
    with fab.cd('opendatacatalog'):
        fab.run('git clone %s' % (OVERLAY_REPO,))


def syncdb():
    with fab.cd('opendatacatalog/Open-Data-Catalog/OpenDataCatalog'):
        fab.sudo('../../bin/python manage.py syncdb', user=DB_USER)

def migrate():
    with fab.cd('opendatacatalog/Open-Data-Catalog/OpenDataCatalog'):
        fab.sudo('../../bin/python manage.py migrate', user=DB_USER)


def catalog():
    unix_user()
    dependencies()
    virtualenv()
    source()
    pip_from_app()
    links_and_permissions()
    postgres()
    local_settings()
    style_overlay()
    syncdb()
    migrate()


def server_dependencies():
    fab.sudo('apt-get install --yes libapache2-mod-wsgi')


def server_config():
    with fab.cd('opendatacatalog'):
        fab.run('cat Open-Data-Catalog/apache.conf.sample'
	        '| sed -e s!{{PATH}}!`pwd`/Open-Data-Catalog!'
		'> /etc/apache2/sites-enabled/000-default')


def static_assets():
    with fab.cd('opendatacatalog/Open-Data-Catalog/OpenDataCatalog'):
        fab.mkdir('static')
        fab.run('../../bin/python manage.py collectstatic --link --noinput')


def restart_server():
    fab.sudo('apache2ctl restart')


def server():
    server_dependencies()
    server_config()
    static_assets()
    restart_server()
