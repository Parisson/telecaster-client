# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Session'
        db.delete_table('telecaster_session')

        # Deleting model 'Department'
        db.delete_table('telecaster_department')

        # Deleting model 'Organization'
        db.delete_table('telecaster_organization')

        # Deleting model 'Professor'
        db.delete_table('telecaster_professor')

        # Deleting model 'Conference'
        db.delete_table('telecaster_conference')


        # Changing field 'Station.conference'
        db.alter_column('telecaster_station', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Conference']))

        # Changing field 'Station.professor'
        db.alter_column('telecaster_station', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Professor']))

        # Renaming column for 'Station.session' to match new field type.
        db.rename_column('telecaster_station', 'session_id', 'session')
        # Changing field 'Station.session'
        db.alter_column('telecaster_station', 'session', self.gf('django.db.models.fields.CharField')(max_length=16))
        # Removing index on 'Station', fields ['session']
        #db.delete_index('telecaster_station', ['session_id'])


        # Changing field 'Station.department'
        db.alter_column('telecaster_station', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Department']))

        # Changing field 'Station.organization'
        db.alter_column('telecaster_station', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['teleforma.Organization']))
    def backwards(self, orm):
        # Adding index on 'Station', fields ['session']
        db.create_index('telecaster_station', ['session_id'])

        # Adding model 'Session'
        db.create_table('telecaster_session', (
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('telecaster', ['Session'])

        # Adding model 'Department'
        db.create_table('telecaster_department', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('telecaster', ['Department'])

        # Adding model 'Organization'
        db.create_table('telecaster_organization', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('telecaster', ['Organization'])

        # Adding model 'Professor'
        db.create_table('telecaster_professor', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('telecaster', ['Professor'])

        # Adding model 'Conference'
        db.create_table('telecaster_conference', (
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='conferences', to=orm['telecaster.Department'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('telecaster', ['Conference'])


        # Changing field 'Station.conference'
        db.alter_column('telecaster_station', 'conference_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telecaster.Conference']))

        # Changing field 'Station.professor'
        db.alter_column('telecaster_station', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telecaster.Professor']))

        # Renaming column for 'Station.session' to match new field type.
        db.rename_column('telecaster_station', 'session', 'session_id')
        # Changing field 'Station.session'
        db.alter_column('telecaster_station', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telecaster.Session']))

        # Changing field 'Station.department'
        db.alter_column('telecaster_station', 'department_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telecaster.Department']))

        # Changing field 'Station.organization'
        db.alter_column('telecaster_station', 'organization_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['telecaster.Organization']))
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
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 25, 0, 0)'}),
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
        'telecaster.record': {
            'Meta': {'object_name': 'Record'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'records'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['telecaster.Station']"})
        },
        'telecaster.station': {
            'Meta': {'object_name': 'Station'},
            'comment': ('telecaster.models.ShortTextField', [], {'blank': 'True'}),
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['teleforma.Conference']"}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['teleforma.Department']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['teleforma.Organization']"}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'station'", 'null': 'True', 'to': "orm['teleforma.Professor']"}),
            'public_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'}),
            'started': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'teleforma.conference': {
            'Meta': {'ordering': "['-date_begin']", 'object_name': 'Conference'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.Course']"}),
            'course_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'conference'", 'to': "orm['teleforma.CourseType']"}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['teleforma.Professor']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'conference'", 'null': 'True', 'to': "orm['teleforma.Room']"}),
            'session': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '16'})
        },
        'teleforma.course': {
            'Meta': {'ordering': "['number']", 'object_name': 'Course'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['teleforma.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magistral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'obligation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'synthesis_note': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.coursetype': {
            'Meta': {'object_name': 'CourseType', 'db_table': "'teleforma_course_type'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.department': {
            'Meta': {'object_name': 'Department'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department'", 'to': "orm['teleforma.Organization']"})
        },
        'teleforma.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'teleforma.professor': {
            'Meta': {'object_name': 'Professor'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'professor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['teleforma.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professor'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'teleforma.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room'", 'to': "orm['teleforma.Organization']"})
        }
    }

    complete_apps = ['telecaster']
