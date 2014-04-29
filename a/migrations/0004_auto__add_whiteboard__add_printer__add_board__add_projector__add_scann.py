# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WhiteBoard'
        db.create_table(u'a_whiteboard', (
            (u'board_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Board'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['WhiteBoard'])

        # Adding model 'Printer'
        db.create_table(u'a_printer', (
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Printer'])

        # Adding model 'Board'
        db.create_table(u'a_board', (
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Board'])

        # Adding M2M table for field notes on 'Board'
        m2m_table_name = db.shorten_name(u'a_board_notes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('board', models.ForeignKey(orm[u'a.board'], null=False)),
            ('note', models.ForeignKey(orm[u'a.note'], null=False))
        ))
        db.create_unique(m2m_table_name, ['board_id', 'note_id'])

        # Adding model 'Projector'
        db.create_table(u'a_projector', (
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Projector'])

        # Adding model 'Scanner'
        db.create_table(u'a_scanner', (
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Scanner'])

        # Adding model 'Note'
        db.create_table(u'a_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'a', ['Note'])

        # Adding model 'BlackBoard'
        db.create_table(u'a_blackboard', (
            (u'board_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Board'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['BlackBoard'])


    def backwards(self, orm):
        # Deleting model 'WhiteBoard'
        db.delete_table(u'a_whiteboard')

        # Deleting model 'Printer'
        db.delete_table(u'a_printer')

        # Deleting model 'Board'
        db.delete_table(u'a_board')

        # Removing M2M table for field notes on 'Board'
        db.delete_table(db.shorten_name(u'a_board_notes'))

        # Deleting model 'Projector'
        db.delete_table(u'a_projector')

        # Deleting model 'Scanner'
        db.delete_table(u'a_scanner')

        # Deleting model 'Note'
        db.delete_table(u'a_note')

        # Deleting model 'BlackBoard'
        db.delete_table(u'a_blackboard')


    models = {
        u'a.blackboard': {
            'Meta': {'object_name': 'BlackBoard', '_ormbases': [u'a.Board']},
            u'board_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Board']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'a.board': {
            'Meta': {'object_name': 'Board', '_ormbases': [u'a.Equipment']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Note']", 'symmetrical': 'False'})
        },
        u'a.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['a.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'a.equipment': {
            'Meta': {'object_name': 'Equipment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8'})
        },
        u'a.note': {
            'Meta': {'object_name': 'Note'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'a.poll': {
            'Meta': {'object_name': 'Poll'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'a.printer': {
            'Meta': {'object_name': 'Printer', '_ormbases': [u'a.Equipment']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'a.projector': {
            'Meta': {'object_name': 'Projector', '_ormbases': [u'a.Equipment']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'a.reservation': {
            'Meta': {'object_name': 'Reservation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['a.Room']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['a.Term']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'a.room': {
            'Meta': {'object_name': 'Room'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Equipment']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Term']", 'symmetrical': 'False'})
        },
        u'a.scanner': {
            'Meta': {'object_name': 'Scanner', '_ormbases': [u'a.Equipment']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'a.term': {
            'Meta': {'unique_together': "(('date', 'begin_time', 'end_time'),)", 'object_name': 'Term'},
            'begin_time': ('django.db.models.fields.TimeField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'a.whiteboard': {
            'Meta': {'object_name': 'WhiteBoard', '_ormbases': [u'a.Board']},
            u'board_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Board']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['a']