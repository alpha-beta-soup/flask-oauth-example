#!flask/bin/python

'''
SQLALhemy-migrate ceates a migration by comparing the structure of the DB
against the structure of the models. The differences between the two are
recorded as a migration script inside the migration repository. The migration
script knows how to apply a migration or undo it, so it is possible to upgrade
or downgrade a database format.

Tips to make this easy for SQLALhemy-migrate:
 - Never rename existing fields (only add and remove, and change types)
 - Always review the generated migration script
 - Always have a backup, use a development DB first
'''

import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(
    SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
    tmp_module.meta, db.metadata
)
open(migration, 'wt').write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print("New migration saved as {}".format(migration))
print("Current database version: {}".format(v))
