# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TimestampedModel'
        db.create_table('project_timestampedmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('project', ['TimestampedModel'])

        # Adding model 'Meeting'
        db.create_table('project_meeting', (
            ('timestampedmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.TimestampedModel'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('begin_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('venue_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('venue_additional', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('project', ['Meeting'])

        # Adding M2M table for field speakers on 'Meeting'
        db.create_table('project_meeting_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm['project.meeting'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('project_meeting_speakers', ['meeting_id', 'user_id'])

        # Adding M2M table for field attendees on 'Meeting'
        db.create_table('project_meeting_attendees', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm['project.meeting'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('project_meeting_attendees', ['meeting_id', 'user_id'])

        # Adding model 'MeetingTag'
        db.create_table('project_meetingtag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('project', ['MeetingTag'])


    def backwards(self, orm):
        
        # Deleting model 'TimestampedModel'
        db.delete_table('project_timestampedmodel')

        # Deleting model 'Meeting'
        db.delete_table('project_meeting')

        # Removing M2M table for field speakers on 'Meeting'
        db.delete_table('project_meeting_speakers')

        # Removing M2M table for field attendees on 'Meeting'
        db.delete_table('project_meeting_attendees')

        # Deleting model 'MeetingTag'
        db.delete_table('project_meetingtag')


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
        'project.meeting': {
            'Meta': {'object_name': 'Meeting', '_ormbases': ['project.TimestampedModel']},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'attending_meetings'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'begin_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'speaking_meetings'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'timestampedmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['project.TimestampedModel']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'venue_additional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'venue_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'project.meetingtag': {
            'Meta': {'object_name': 'MeetingTag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'project.timestampedmodel': {
            'Meta': {'object_name': 'TimestampedModel'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['project']