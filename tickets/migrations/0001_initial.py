# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default=b'', max_length=100, blank=True)),
                ('description', models.TextField()),
                ('progress', models.IntegerField(default=0)),
                ('priority', models.IntegerField(default=1)),
                ('hardness', models.IntegerField(default=1)),
                ('owner', models.ForeignKey(related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
    ]
