# Generated by Django 3.1.7 on 2021-08-13 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0021_auto_20210809_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='message',
        ),
        migrations.RemoveField(
            model_name='document',
            name='date',
        ),
        migrations.RemoveField(
            model_name='document',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='document',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='document',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='document',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='lawcase',
            name='extra_help',
        ),
    ]