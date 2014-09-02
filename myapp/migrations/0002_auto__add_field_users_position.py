# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Users.position'
        db.add_column(u'myapp_users', 'position',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 9, 1, 0, 0), max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Users.position'
        db.delete_column(u'myapp_users', 'position')


    models = {
        'myapp.rooms': {
            'Meta': {'object_name': 'Rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'myapp.users': {
            'Meta': {'object_name': 'Users'},
            'date_birthday': ('django.db.models.fields.DateField', [], {}),
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['myapp']