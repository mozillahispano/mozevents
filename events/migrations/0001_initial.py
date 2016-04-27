# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eventDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('regStartDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('regEndDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('places', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('commentsUrl', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitterTag', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('queueActive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('queueSize', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('queueWaitTime', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding model 'Registration'
        db.create_table(u'events_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('familyName', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('press', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('volunteer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('mailme', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Invited', max_length=9)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'events', ['Registration'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Deleting model 'Registration'
        db.delete_table(u'events_registration')


    models = {
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'commentsUrl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'queueActive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'queueSize': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'queueWaitTime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'regEndDate': ('django.db.models.fields.DateTimeField', [], {}),
            'regStartDate': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'twitterTag': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'events.registration': {
            'Meta': {'object_name': 'Registration'},
            'creationDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'familyName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailme': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'press': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Invited'", 'max_length': '9'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['events']