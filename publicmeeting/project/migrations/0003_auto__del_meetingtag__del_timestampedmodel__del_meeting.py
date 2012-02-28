# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'MeetingTag'
        db.delete_table('project_meetingtag')

        # Deleting model 'TimestampedModel'
        db.delete_table('project_timestampedmodel')

        # Deleting model 'Meeting'
        db.delete_table('project_meeting')

        # Removing M2M table for field speakers on 'Meeting'
        db.delete_table('project_meeting_speakers')

        # Removing M2M table for field attendees on 'Meeting'
        db.delete_table('project_meeting_attendees')


    def backwards(self, orm):
        
        # Adding model 'MeetingTag'
        db.create_table('project_meetingtag', (
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('project', ['MeetingTag'])

        # Adding model 'TimestampedModel'
        db.create_table('project_timestampedmodel', (
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('project', ['TimestampedModel'])

        # Adding model 'Meeting'
        db.create_table('project_meeting', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('venue_additional', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('begin_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('timestampedmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['project.TimestampedModel'], unique=True, primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(blank=True, max_length=50, db_index=True)),
            ('venue_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
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


    models = {
        
    }

    complete_apps = ['project']
