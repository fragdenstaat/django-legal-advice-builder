# Generated by Django 3.1.7 on 2021-05-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0008_auto_20210507_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawcase',
            name='save_answers',
            field=models.BooleanField(default=False),
        ),
    ]
