# Generated by Django 3.1.7 on 2021-05-14 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0009_lawcase_save_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='success_conditions',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]