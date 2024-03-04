# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='video_file',
            new_name='file',
        ),
        migrations.RemoveField(
            model_name='video',
            name='name',
        ),
    ]
