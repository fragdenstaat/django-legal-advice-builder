# Generated by Django 3.1.7 on 2021-07-19 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0009_auto_20210717_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='failure_message',
        ),
        migrations.RemoveField(
            model_name='question',
            name='success_message',
        ),
        migrations.RemoveField(
            model_name='question',
            name='unsure_message',
        ),
        migrations.RemoveField(
            model_name='questionaire',
            name='failure_message',
        ),
    ]