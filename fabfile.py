from fabric.api import task, env, run, local, roles, cd, execute, hide, puts, sudo, abort
import posixpath
import re
import fabtools
import datetime

env.project_name = 'pymallorca'
env.repository = 'git@github.com:pymallorca/pymallorca.git'
env.local_branch = 'master'
env.remote_ref = 'origin/master'
env.requirements_file = 'requirements.txt'
env.restart_command = 'touch {project_name}.reload'.format(**env)
env.restart_sudo = True


#==============================================================================
# Tasks which set up deployment environments
#==============================================================================

@task
def prod():
    """
    Use the live deployment environment.
    """
    server = 'pymallorca.org'
    env.host_string = server
    env.user_app = 'pymallorca'
    env.port = 2232
    env.project_dir = '/var/pywww/pymallorca'
    env.project_codedir = '/var/pywww/pymallorca/code'
    env.virtualenv_dir = '/var/pywww/pymallorca/.virtualenvs/pymallorca'

# Set the default environment.
prod()


#==============================================================================
# Actual tasks
#==============================================================================

@task
def update():
    git_pull()
    django('migrate')
    django('collectstatic --noinput')
    restart()


#==============================================================================
# Helper functions
#==============================================================================

def django(command):
    """
    Run a Django manage.py command on the server.
    """
    env.user = env.user_app
    with cd(env.project_dir):
        run('django_execute {dj_command}'.format(dj_command=command, **env))

def git_pull():
    """
    Update the code from repository
    """
    env.user = env.user_app
    with cd(env.project_codedir):
        run('git pull')

def restart():
    env.user = env.user_app
    with cd(env.project_dir):
        run(env.restart_command)

def create_user():
    env.user = env.user_system
    # Create DB user if it does not exist
    if not fabtools.postgres.user_exists(env.postgres_username):
        fabtools.postgres.create_user(env.postgres_username, password=env.postgres_password)
        puts("Creado usuario para postgres %s" % env.postgres_username)


def create_database():
    env.user = env.user_system
    # Create DB if it does not exist
    if not fabtools.postgres.database_exists(env.postgres_database):
        sudo('echo "CREATE DATABASE %s;" |psql' % env.postgres_database, user='postgres')
        puts("Creada base de datos postgres %s" % env.postgres_database)


def drop_database():
    env.user = env.user_system
    # Drop DB if exist
    if fabtools.postgres.database_exists(env.postgres_database):
        puts("Borrando la base de datos postgres %s" % env.postgres_database)
        sudo('echo "DROP DATABASE %s;" |psql' % env.postgres_database, user='postgres')

def recreate_database():
    drop_database()
    create_database()


def backup_database_env():
    # Necesario root
    env.user = env.user_system

    # Creamos la ruta para el dump si no exsite
    if not fabtools.files.is_dir(env.postgres_dumps_dir):
        run('mkdir %s' % env.postgres_dumps_dir)

    with cd('~postgres'):
        puts("Guardando un dump de la base de datos para el entorno")
        now = datetime.date.today().strftime("%d-%m-%Y")
        sudo('pg_dump -O dbname={postgres_database} '
             '-f {postgres_database}-{now}.sql'.format(now=now, **env), user='postgres' )
        run('mv {postgres_database}-{now}.sql {postgres_dumps_dir}/'.format(now=now, **env))
        run('chown {user_app}:{user_app} -R {postgres_dumps_dir}'.format(**env))

def restore_database():
        now = datetime.date.today().strftime("%d-%m-%Y")
        if not fabtools.files.is_file('{postgres_dumps_dir_production}/{postgres_database_production}-{now}.sql'.format(now=now, **env)):
            puts('No exsite fichero de dump de produccion de hoy')
            puts('Debes ejecutar el backup de produccion antes de lanzar este comando')
        else:
            with cd('~postgres'):
                run('cp {postgres_dumps_dir_production}/{postgres_database_production}-{now}.sql .'.format(now=now, **env))
                run('chown postgres:postgres {postgres_database_production}-{now}.sql'.format(now=now, **env))
                sudo('psql {postgres_database} < {postgres_database_production}-{now}.sql'.format(now=now, **env), user='postgres')
                sudo('rm {postgres_database_production}-{now}.sql'.format(now=now, **env), user='postgres')
                sudo('psql {postgres_database} < {project_dir}/anonymize_testdatabase.sql'.format(**env), user='postgres')
                sudo('for tbl in `psql -qAt -c "select tablename from'
                     ' pg_tables where schemaname = \'public\';" {postgres_database}` ;'
                     ' do  psql -c "alter table $tbl owner to {postgres_username}" {postgres_database} ; done'.format(**env),
                     user='postgres')

                sudo('for tbl in `psql -qAt -c "select sequence_name from'
                     ' information_schema.sequences where sequence_schema = \'public\';" {postgres_database}` ;'
                     ' do  psql -c "alter table $tbl owner to {postgres_username}" {postgres_database} ; done'.format(**env),
                     user='postgres')

                sudo('for tbl in `psql -qAt -c "select table_name from '
                     ' information_schema.views where table_schema = \'public\';" {postgres_database}` ;'
                     ' do  psql -c "alter table $tbl owner to {postgres_username}" {postgres_database} ; done'.format(**env),
                     user='postgres')