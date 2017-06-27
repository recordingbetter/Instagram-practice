# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_comment_html_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(max_length=30)),
                ('youtube_thumbnail', models.ImageField(upload_to='youtube_thumbnail')),
                ('youtube_title', models.CharField(max_length=100)),
                ('youtube_description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]