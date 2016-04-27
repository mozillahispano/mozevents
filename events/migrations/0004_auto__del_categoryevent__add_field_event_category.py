# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CategoryEvent'
        db.delete_table(u'events_categoryevent')

        # Adding field 'Event.category'
        db.add_column(u'events_event', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Category'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'CategoryEvent'
        db.create_table(u'events_categoryevent', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Category'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'events', ['CategoryEvent'])

        # Deleting field 'Event.category'
        db.delete_column(u'events_event', 'category_id')


    models = {
        u'events.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Category']", 'null': 'True', 'blank': 'True'}),
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