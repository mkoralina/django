# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Printer'
        db.delete_table(u'a_printer')

        # Deleting model 'Mobile'
        db.delete_table(u'a_mobile')

        # Removing M2M table for field rooms on 'Mobile'
        db.delete_table(db.shorten_name(u'a_mobile_rooms'))

        # Deleting model 'Projector'
        db.delete_table(u'a_projector')

        # Deleting model 'Scanner'
        db.delete_table(u'a_scanner')

        # Deleting field 'Equipment.serial_number'
        db.delete_column(u'a_equipment', 'serial_number')

        # Adding field 'Equipment.id'
        db.add_column(u'a_equipment', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'Equipment.type'
        db.add_column(u'a_equipment', 'type',
                      self.gf('django.db.models.fields.CharField')(default=2, max_length=20),
                      keep_default=False)

        # Deleting field 'Board.equipment_ptr'
        db.delete_column(u'a_board', u'equipment_ptr_id')

        # Adding field 'Board.id'
        db.add_column(u'a_board', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'Board.type'
        db.add_column(u'a_board', 'type',
                      self.gf('django.db.models.fields.CharField')(default='blackboard', max_length=20),
                      keep_default=False)

        # Adding M2M table for field equipment on 'Room'
        m2m_table_name = db.shorten_name(u'a_room_equipment')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('room', models.ForeignKey(orm[u'a.room'], null=False)),
            ('equipment', models.ForeignKey(orm[u'a.equipment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['room_id', 'equipment_id'])


    def backwards(self, orm):
        # Adding model 'Printer'
        db.create_table(u'a_printer', (
            (u'mobile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Mobile'], unique=True)),
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Printer'])

        # Adding model 'Mobile'
        db.create_table(u'a_mobile', (
            ('mobile_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Adding model 'Projector'
        db.create_table(u'a_projector', (
            (u'mobile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Mobile'], unique=True)),
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Projector'])

        # Adding model 'Scanner'
        db.create_table(u'a_scanner', (
            (u'mobile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Mobile'], unique=True)),
            (u'equipment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['a.Equipment'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'a', ['Scanner'])

        # Adding field 'Equipment.serial_number'
        db.add_column(u'a_equipment', 'serial_number',
                      self.gf('django.db.models.fields.IntegerField')(default=2, max_length=8, primary_key=True),
                      keep_default=False)

        # Deleting field 'Equipment.id'
        db.delete_column(u'a_equipment', u'id')

        # Deleting field 'Equipment.type'
        db.delete_column(u'a_equipment', 'type')

        # Adding field 'Board.equipment_ptr'
        db.add_column(u'a_board', u'equipment_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['a.Equipment'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Board.id'
        db.delete_column(u'a_board', u'id')

        # Deleting field 'Board.type'
        db.delete_column(u'a_board', 'type')

        # Removing M2M table for field equipment on 'Room'
        db.delete_table(db.shorten_name(u'a_room_equipment'))


    models = {
        u'a.board': {
            'Meta': {'object_name': 'Board'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['a.Note']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'blackboard'", 'max_length': '20'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
            'equipment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Equipment']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['a.Term']", 'symmetrical': 'False'})
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