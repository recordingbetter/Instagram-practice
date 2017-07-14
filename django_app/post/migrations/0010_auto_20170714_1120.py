# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 02:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0009_post_video'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postlike',
            unique_together=set([('post', 'user')]),
        ),
    ]
