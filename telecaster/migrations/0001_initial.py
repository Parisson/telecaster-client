# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('telecaster_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('telecaster', ['Organization'])

        # Adding model 'Department'
        db.create_table('telecaster_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('telecaster', ['Department'])

        # Adding model 'Conference'
        db.create_table('telecaster_conference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='conferences', to=orm['telecaster.Department'])),
        ))
        db.send_create_signal('telecaster', ['Conference'])

        # Adding model 'Session'
        db.create_table('telecaster_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('telecaster', ['Session'])

        # Adding model 'Professor'
        db.create_table('telecaster_professor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('telecaster', ['Professor'])

        # Adding model 'Station'
        db.create_table('telecaster_station', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='station', null=True, to=orm['telecaster.Organization'])),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='station', null=True, to=orm['telecaster.Department'])),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='station', null=True, to=orm['telecaster.Conference'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='station', null=True, to=orm['telecaster.Session'])),
            ('professor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='station', null=True, to=orm['telecaster.Professor'])),
            ('comment', self.gf('telecaster.models.ShortTextField')(blank=True)),
            ('started', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('datetime_stop', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('telecaster', ['Station'])

        # Adding model 'Record'
        db.create_table('telecaster_record', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='records', null=True, on_delete=models.SET_NULL, to=orm['telecaster.Station'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('telecaster', ['Record'])

    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table('telecaster_organization')

        # Deleting model 'Department'
        db.delete_table('telecaster_department')

        # Deleting model 'Conference'
        db.delete_table('telecaster_conference')

        # Deleting model 'Session'
        db.delete_table('telecaster_session')

        # Deleting model 'Professor'
        db.delete_table('telecaster_professor')

        # Deleting model 'Station'
        db.delete_table('telecaster_station')

        # Deleting model 'Record'
        db.delete_table('telecaster_record')

    models = {
        'telecaster.conference': {
            'Meta': {'object_name': 'Conference'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conferences'", 'to': "orm['telecaster.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'telecaster.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'telecaster.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'telecaster.professor': {
            'Meta': {'object_name': 'Professor'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'telecaster.record': {
            'Meta': {'object_name': 'Record'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'records'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['telecaster.Station']"})
        },
        'telecaster.session': {
            'Meta': {'object_name': 'Session'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'telecaster.station': {
            'Meta': {'object_name': 'Station'},
            'comment': ('telecaster.models.ShortTextField', [], {'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['telecaster.Conference']"}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['telecaster.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['telecaster.Organization']"}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['telecaster.Professor']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['telecaster.Session']"}),
            'started': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['telecaster']