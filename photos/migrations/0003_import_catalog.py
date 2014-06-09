# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import json

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        images = json.loads(file("images.json").read())
        Photo = orm['photos.Photo']
        for image in images:
            photo = Photo(
                filename = image['filename'],
                title = image['title'],
                description = image['description'],
            )
            photo.save()



    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['photos']
    symmetrical = True
