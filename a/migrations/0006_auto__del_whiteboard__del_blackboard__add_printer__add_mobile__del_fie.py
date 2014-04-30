# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WhiteBoard'
        db.delete_table(u'a_whiteboard')

        # Deleting model 'BlackBoard'
        db.delete_table(u'a_blackboard')

        # Adding model 'Printer'
        db.create_table(u'a_printer', (
            (u'mobile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Mobile'], unique=True)),
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Printer'])

        # Adding model 'Mobile'
        db.create_table(u'a_mobile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Mobile'])

        # Adding M2M table for field rooms on 'Mobile'
        m2m_table_name = db.shorten_name(u'a_mobile_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mobile', models.ForeignKey(orm[u'a.mobile'], null=False)),
            ('room', models.ForeignKey(orm[u'a.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mobile_id', 'room_id'])

        # Deleting field 'Equipment.id'
        db.delete_column(u'a_equipment', u'id')

        # Removing M2M table for field rooms on 'Equipment'
        db.delete_table(db.shorten_name(u'a_equipment_rooms'))


        # Changing field 'Equipment.serial_number'
        db.alter_column(u'a_equipment', 'serial_number', self.gf('django.db.models.fields.SlugField')(max_length=8, primary_key=True))
        # Adding unique constraint on 'Equipment', fields ['serial_number']
        db.create_unique(u'a_equipment', ['serial_number'])

        # Adding field 'Board.color'
        db.add_column(u'a_board', 'color',
                      self.gf('django.db.models.fields.CharField')(default='black', max_length=20),
                      keep_default=False)

        # Adding field 'Projector.mobile_ptr'
        db.add_column(u'a_projector', u'mobile_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['a.Mobile'], unique=True),
                      keep_default=False)

        # Adding field 'Scanner.mobile_ptr'
        db.add_column(u'a_scanner', u'mobile_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['a.Mobile'], unique=True),
                      keep_default=False)

        # Adding M2M table for field boards on 'Room'
        m2m_table_name = db.shorten_name(u'a_room_boards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm[u'a.room'], null=False)),
            ('board', models.ForeignKey(orm[u'a.board'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'board_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Equipment', fields ['serial_number']
        db.delete_unique(u'a_equipment', ['serial_number'])

        # Adding model 'WhiteBoard'
        db.create_table(u'a_whiteboard', (
            (u'board_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Board'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['WhiteBoard'])

        # Adding model 'BlackBoard'
        db.create_table(u'a_blackboard', (
            (u'board_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Board'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['BlackBoard'])

        # Deleting model 'Printer'
        db.delete_table(u'a_printer')

        # Deleting model 'Mobile'
        db.delete_table(u'a_mobile')

        # Removing M2M table for field rooms on 'Mobile'
        db.delete_table(db.shorten_name(u'a_mobile_rooms'))

        # Adding field 'Equipment.id'
        db.add_column(u'a_equipment', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Adding M2M table for field rooms on 'Equipment'
        m2m_table_name = db.shorten_name(u'a_equipment_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('equipment', models.ForeignKey(orm[u'a.equipment'], null=False)),
            ('room', models.ForeignKey(orm[u'a.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['equipment_id', 'room_id'])


        # Changing field 'Equipment.serial_number'
        db.alter_column(u'a_equipment', 'serial_number', self.gf('django.db.models.fields.SlugField')(max_length=8))
        # Deleting field 'Board.color'
        db.delete_column(u'a_board', 'color')

        # Deleting field 'Projector.mobile_ptr'
        db.delete_column(u'a_projector', u'mobile_ptr_id')

        # Deleting field 'Scanner.mobile_ptr'
        db.delete_column(u'a_scanner', u'mobile_ptr_id')

        # Removing M2M table for field boards on 'Room'
        db.delete_table(db.shorten_name(u'a_room_boards'))


    models = {
        u'a.board': {
            'Meta': {'object_name': 'Board', '_ormbases': [u'a.Equipment']},
            'color': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '20'}),
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['a.Note']", 'null': 'True', 'blank': 'True'})
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
            'serial_number': ('django.db.models.fields.SlugField', [], {'max_length': '8', 'primary_key': 'True'})
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
            'Meta': {'object_name': 'Printer', '_ormbases': [u'a.Equipment', u'a.Mobile']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
            u'mobile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Mobile']", 'unique': 'True'})
        },
        u'a.projector': {
            'Meta': {'object_name': 'Projector', '_ormbases': [u'a.Equipment', u'a.Mobile']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
            u'mobile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Mobile']", 'unique': 'True'})
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
            'Meta': {'object_name': 'Scanner', '_ormbases': [u'a.Equipment', u'a.Mobile']},
            u'equipment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Equipment']", 'unique': 'True', 'primary_key': 'True'}),
            u'mobile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['a.Mobile']", 'unique': 'True'})
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