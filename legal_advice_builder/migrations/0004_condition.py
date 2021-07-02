# Generated by Django 3.1.7 on 2021-06-23 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0003_auto_20210603_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_option', models.CharField(max_length=500)),
                ('if_value', models.CharField(max_length=500)),
                ('then_value', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legal_advice_builder.question')),
            ],
            options={
                'unique_together': {('question', 'if_value', 'then_value')},
            },
        ),
    ]
