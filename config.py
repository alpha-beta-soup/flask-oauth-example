import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASEDIR, 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WRF_CSRF_ENABLED = True # Activates the cross-site request forgery prevention
SECRET_KEY = 'you-will-never-guess'

OAUTH_CREDENTIALS = {
    'twitter': {
        'id': 'getyourownid',
        'secret': 'getyourownsecret'
    }
}
