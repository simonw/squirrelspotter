# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Spotter', fields ['fb_id']
        db.create_index('spotter_spotter', ['fb_id'])


    def backwards(self, orm):
        # Removing index on 'Spotter', fields ['fb_id']
        db.delete_index('spotter_spotter', ['fb_id'])


    models = {
        'spotter.spot': {
            'Meta': {'object_name': 'Spot'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'geohash': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'spotter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spotter.Spotter']"})
        },
        'spotter.spotter': {
            'Meta': {'object_name': 'Spotter'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'fb_access_token_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'fb_json': ('django.db.models.fields.TextField', [], {}),
            'first_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone_number_token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spotter']