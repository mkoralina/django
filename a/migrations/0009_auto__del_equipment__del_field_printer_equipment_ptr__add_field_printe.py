# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Equipment'
        db.delete_table(u'a_equipment')

        # Deleting field 'Printer.equipment_ptr'
        db.delete_column(u'a_printer', u'equipment_ptr_id')

        # Adding field 'Printer.name'
        db.add_column(u'a_printer', 'name',
                      self.gf('django.db.models.fields.CharField')(default='printer', max_length=20),
                      keep_default=False)

        # Adding field 'Printer.serial_number'
        db.add_column(u'a_printer', 'serial_number',
                      self.gf('django.db.models.fields.IntegerField')(default=35254, max_length=8, primary_key=True),
                      keep_default=False)

        # Deleting field 'Board.equipment_ptr'
        db.delete_column(u'a_board', u'equipment_ptr_id')

        # Adding field 'Board.name'
        db.add_column(u'a_board', 'name',
                      self.gf('django.db.models.fields.CharField')(default='board', max_length=20),
                      keep_default=False)

        # Adding field 'Board.serial_number'
        db.add_column(u'a_board', 'serial_number',
                      self.gf('django.db.models.fields.IntegerField')(default=352, max_length=8, primary_key=True),
                      keep_default=False)

        # Deleting field 'Projector.equipment_ptr'
        db.delete_column(u'a_projector', u'equipment_ptr_id')

        # Adding field 'Projector.name'
        db.add_column(u'a_projector', 'name',
                      self.gf('django.db.models.fields.CharField')(default='projector', max_length=20),
                      keep_default=False)

        # Adding field 'Projector.serial_number'
        db.add_column(u'a_projector', 'serial_number',
                      self.gf('django.db.models.fields.IntegerField')(default=345, max_length=8, primary_key=True),
                      keep_default=False)

        # Deleting field 'Scanner.equipment_ptr'
        db.delete_column(u'a_scanner', u'equipment_ptr_id')

        # Adding field 'Scanner.name'
        db.add_column(u'a_scanner', 'name',
                      self.gf('django.db.models.fields.CharField')(default='scanner', max_length=20),
                      keep_default=False)

        # Adding field 'Scanner.serial_number'
        db.add_column(u'a_scanner', 'serial_number',
                      self.gf('django.db.models.fields.IntegerField')(default=876, max_length=8, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Equipment'
        db.create_table(u'a_equipment', (
            ('serial_number', self.gf('django.db.models.fields.IntegerField')(max_length=8, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'a', ['Equipment'])

        # Adding field 'Printer.equipment_ptr'
        db.add_column(u'a_printer', u'equipment_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['a.Equipment'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Printer.name'
        db.delete_column(u'a_printer', 'name')

        # Deleting field 'Printer.serial_number'
        db.delete_column(u'a_printer', 'serial_number')

        # Adding field 'Board.equipment_ptr'
        db.add_column(u'a_board', u'equipment_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['a.Equipment'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Board.name'
        db.delete_column(u'a_board', 'name')

        # Deleting field 'Board.serial_number'
        db.delete_column(u'a_board', 'serial_number')

        # Adding field 'Projector.equipment_ptr'
        db.add_column(u'a_projector', u'equipment_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=3, to=orm['a.Equipment'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Projector.name'
        db.delete_column(u'a_projector', 'name')

        # Deleting field 'Projector.serial_number'
        db.delete_column(u'a_projector', 'serial_number')

        # Adding field 'Scanner.equipment_ptr'
        db.add_column(u'a_scanner', u'equipment_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=432, to=orm['a.Equipment'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Scanner.name'
        db.delete_column(u'a_scanner', 'name')

        # Deleting field 'Scanner.serial_number'
        db.delete_column(u'a_scanner', 'serial_number')


    models = {
        u'a.board': {
            'Meta': {'object_name': 'Board'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['a.Note']", 'null': 'True', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'primary_key': 'True'})
        },
        u'a.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['a.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'a.mobile': {
            'Meta': {'object_name': 'Mobile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['a.Room']", 'null': 'True', 'blank': 'True'})
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
            'Meta': {'object_name': 'Printer', '_ormbases': [u'a.Mobile']},
            u'mobile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Mobile']", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'primary_key': 'True'})
        },
        u'a.projector': {
            'Meta': {'object_name': 'Projector', '_ormbases': [u'a.Mobile']},
            u'mobile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Mobile']", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'primary_key': 'True'})
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
            'boards': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Board']", 'symmetrical': 'False'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Term']", 'symmetrical': 'False'})
        },
        u'a.scanner': {
            'Meta': {'object_name': 'Scanner', '_ormbases': [u'a.Mobile']},
            u'mobile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Mobile']", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'serial_number': ('django.db.models.fields.IntegerField', [], {'max_length': '8', 'primary_key': 'True'})
        },
        u'a.term': {
            'Meta': {'unique_together': "(('date', 'begin_time', 'end_time'),)", 'object_name': 'Term'},
            'begin_time': ('django.db.models.fields.TimeField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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