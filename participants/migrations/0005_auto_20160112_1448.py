# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 14:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0004_auto_20160112_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='venue_preferences',
        ),
        migrations.RemoveField(
            model_name='team',
            name='venue_preferences',
        ),
    ]