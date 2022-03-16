# Generated by Django 3.2.8 on 2022-01-26 16:34

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0006_lawcase_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answers',
            field=models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]