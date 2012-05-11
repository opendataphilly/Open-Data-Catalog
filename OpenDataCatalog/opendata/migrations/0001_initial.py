# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('opendata_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('opendata', ['Tag'])

        # Adding model 'DataType'
        db.create_table('opendata_datatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('opendata', ['DataType'])

        # Adding model 'UrlType'
        db.create_table('opendata_urltype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('opendata', ['UrlType'])

        # Adding model 'UpdateFrequency'
        db.create_table('opendata_updatefrequency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_frequency', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('opendata', ['UpdateFrequency'])

        # Adding model 'CoordSystem'
        db.create_table('opendata_coordsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('EPSG_code', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal('opendata', ['CoordSystem'])

        # Adding model 'Resource'
        db.create_table('opendata_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time_period', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('division', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('usage', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('contact_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('updates', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opendata.UpdateFrequency'], null=True, blank=True)),
            ('area_of_interest', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_by', to=orm['auth.User'])),
            ('last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updated_by', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('metadata_contact', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('metadata_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('update_frequency', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('data_formats', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('proj_coord_sys', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('opendata', ['Resource'])

        # Adding M2M table for field tags on 'Resource'
        db.create_table('opendata_resource_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['opendata.resource'], null=False)),
            ('tag', models.ForeignKey(orm['opendata.tag'], null=False))
        ))
        db.create_unique('opendata_resource_tags', ['resource_id', 'tag_id'])

        # Adding M2M table for field data_types on 'Resource'
        db.create_table('opendata_resource_data_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['opendata.resource'], null=False)),
            ('datatype', models.ForeignKey(orm['opendata.datatype'], null=False))
        ))
        db.create_unique('opendata_resource_data_types', ['resource_id', 'datatype_id'])

        # Adding M2M table for field coord_sys on 'Resource'
        db.create_table('opendata_resource_coord_sys', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resource', models.ForeignKey(orm['opendata.resource'], null=False)),
            ('coordsystem', models.ForeignKey(orm['opendata.coordsystem'], null=False))
        ))
        db.create_unique('opendata_resource_coord_sys', ['resource_id', 'coordsystem_id'])

        # Adding model 'Url'
        db.create_table('opendata_url', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url_label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opendata.UrlType'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opendata.Resource'])),
        ))
        db.send_create_signal('opendata', ['Url'])

        # Adding model 'UrlImage'
        db.create_table('opendata_urlimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opendata.Url'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('opendata', ['UrlImage'])

        # Adding model 'Idea'
        db.create_table('opendata_idea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='idea_created_by', to=orm['auth.User'])),
            ('created_by_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='idea_updated_by', to=orm['auth.User'])),
            ('updated_by_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('opendata', ['Idea'])

        # Adding M2M table for field resources on 'Idea'
        db.create_table('opendata_idea_resources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm['opendata.idea'], null=False)),
            ('resource', models.ForeignKey(orm['opendata.resource'], null=False))
        ))
        db.create_unique('opendata_idea_resources', ['idea_id', 'resource_id'])

        # Adding model 'IdeaImage'
        db.create_table('opendata_ideaimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opendata.Idea'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('home_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('opendata', ['IdeaImage'])

        # Adding model 'Submission'
        db.create_table('opendata_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('sent_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('opendata', ['Submission'])

        # Adding model 'TwitterCache'
        db.create_table('opendata_twittercache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('opendata', ['TwitterCache'])

        # Adding model 'ODPUserProfile'
        db.create_table('opendata_odpuserprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('can_notify', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('opendata', ['ODPUserProfile'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('opendata_tag')

        # Deleting model 'DataType'
        db.delete_table('opendata_datatype')

        # Deleting model 'UrlType'
        db.delete_table('opendata_urltype')

        # Deleting model 'UpdateFrequency'
        db.delete_table('opendata_updatefrequency')

        # Deleting model 'CoordSystem'
        db.delete_table('opendata_coordsystem')

        # Deleting model 'Resource'
        db.delete_table('opendata_resource')

        # Removing M2M table for field tags on 'Resource'
        db.delete_table('opendata_resource_tags')

        # Removing M2M table for field data_types on 'Resource'
        db.delete_table('opendata_resource_data_types')

        # Removing M2M table for field coord_sys on 'Resource'
        db.delete_table('opendata_resource_coord_sys')

        # Deleting model 'Url'
        db.delete_table('opendata_url')

        # Deleting model 'UrlImage'
        db.delete_table('opendata_urlimage')

        # Deleting model 'Idea'
        db.delete_table('opendata_idea')

        # Removing M2M table for field resources on 'Idea'
        db.delete_table('opendata_idea_resources')

        # Deleting model 'IdeaImage'
        db.delete_table('opendata_ideaimage')

        # Deleting model 'Submission'
        db.delete_table('opendata_submission')

        # Deleting model 'TwitterCache'
        db.delete_table('opendata_twittercache')

        # Deleting model 'ODPUserProfile'
        db.delete_table('opendata_odpuserprofile')


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
        'opendata.coordsystem': {
            'EPSG_code': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'Meta': {'ordering': "['EPSG_code']", 'object_name': 'CoordSystem'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'opendata.datatype': {
            'Meta': {'ordering': "['data_type']", 'object_name': 'DataType'},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'opendata.idea': {
            'Meta': {'object_name': 'Idea'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'idea_created_by'", 'to': "orm['auth.User']"}),
            'created_by_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['opendata.Resource']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'idea_updated_by'", 'to': "orm['auth.User']"}),
            'updated_by_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'opendata.ideaimage': {
            'Meta': {'object_name': 'IdeaImage'},
            'home_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata.Idea']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'opendata.odpuserprofile': {
            'Meta': {'object_name': 'ODPUserProfile'},
            'can_notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'opendata.resource': {
            'Meta': {'object_name': 'Resource'},
            'area_of_interest': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'contact_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'coord_sys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['opendata.CoordSystem']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_by'", 'to': "orm['auth.User']"}),
            'data_formats': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'data_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['opendata.DataType']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updated_by'", 'to': "orm['auth.User']"}),
            'metadata_contact': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'metadata_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'proj_coord_sys': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['opendata.Tag']", 'null': 'True', 'blank': 'True'}),
            'time_period': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'update_frequency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updates': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata.UpdateFrequency']", 'null': 'True', 'blank': 'True'}),
            'usage': ('django.db.models.fields.TextField', [], {})
        },
        'opendata.submission': {
            'Meta': {'object_name': 'Submission'},
            'email_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'opendata.tag': {
            'Meta': {'ordering': "['tag_name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'opendata.twittercache': {
            'Meta': {'object_name': 'TwitterCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'opendata.updatefrequency': {
            'Meta': {'ordering': "['update_frequency']", 'object_name': 'UpdateFrequency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_frequency': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'opendata.url': {
            'Meta': {'object_name': 'Url'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata.Resource']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata.UrlType']"})
        },
        'opendata.urlimage': {
            'Meta': {'object_name': 'UrlImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata.Url']"})
        },
        'opendata.urltype': {
            'Meta': {'ordering': "['url_type']", 'object_name': 'UrlType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['opendata']