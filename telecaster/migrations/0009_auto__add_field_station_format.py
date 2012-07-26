# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Station.format'
        db.add_column('telecaster_station', 'format',
                      self.gf('telemeta.models.core.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Station.format'
        db.delete_column('telecaster_station', 'format')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notes.note': {
            'Meta': {'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 7, 26, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rendered_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notes.Topic']"})
        },
        'notes.topic': {
            'Meta': {'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'telecaster.osc': {
            'Meta': {'object_name': 'OSC'},
            'host': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'port': ('telemeta.models.core.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'telecaster.station': {
            'Meta': {'object_name': 'Station'},
            'conference': ('telemeta.models.core.ForeignKey', [], {'related_name': "'station'", 'to': "orm['teleforma.Conference']"}),
            'deefuzzer_file': ('telemeta.models.core.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'format': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osc': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['telecaster.OSC']"}),
            'pid': ('telemeta.models.core.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'public_id': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'record_dir': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'started': ('telemeta.models.core.BooleanField', [], {'default': 'False'})
        },
        'teleforma.conference': {
            'Meta': {'ordering': "['-date_begin']", 'object_name': 'Conference'},
            'comment': ('teleforma.models.ShortTextField', [], {'max_length': '255', 'blank': 'True'}),
            'course': ('telemeta.models.core.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('telemeta.models.core.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.CourseType']"}),
            'date_begin': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_end': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('telemeta.models.core.ForeignKey', [], {'related_name': "'conference'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['teleforma.Professor']", 'blank': 'True', 'null': 'True'}),
            'public_id': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'room': ('telemeta.models.core.ForeignKey', [], {'default': 'None', 'related_name': "'conference'", 'null': 'True', 'blank': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('telemeta.models.core.CharField', [], {'default': "'1'", 'max_length': '16', 'blank': 'True'})
        },
        'teleforma.course': {
            'Meta': {'ordering': "['number']", 'object_name': 'Course'},
            'code': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'date_modified': ('telemeta.models.core.DateTimeField', [], {'default': 'None', 'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'department': ('telemeta.models.core.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'number': ('telemeta.models.core.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'obligation': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'synthesis_note': ('telemeta.models.core.BooleanField', [], {'default': 'False'}),
            'title': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.coursetype': {
            'Meta': {'object_name': 'CourseType', 'db_table': "'teleforma_course_type'"},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'domain': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'organization': ('telemeta.models.core.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'teleforma.professor': {
            'Meta': {'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('telemeta.models.core.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('telemeta.models.core.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'organization': ('telemeta.models.core.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
        }
    }

    complete_apps = ['telecaster']