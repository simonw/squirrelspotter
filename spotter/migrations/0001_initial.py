# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Spotter'
        db.create_table('spotter_spotter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fb_access_token', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fb_access_token_expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone_number_token', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('spotter', ['Spotter'])

        # Adding model 'Spot'
        db.create_table('spotter_spot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('spotter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spotter.Spotter'])),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('geohash', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('location_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('spotter', ['Spot'])


    def backwards(self, orm):
        # Deleting model 'Spotter'
        db.delete_table('spotter_spotter')

        # Deleting model 'Spot'
        db.delete_table('spotter_spot')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone_number_token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spotter']