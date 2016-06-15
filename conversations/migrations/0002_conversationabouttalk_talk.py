# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-15 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proposals', '0001_initial'),
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationabouttalk',
            name='talk',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conversation', to='proposals.Talk'),
        ),
    ]