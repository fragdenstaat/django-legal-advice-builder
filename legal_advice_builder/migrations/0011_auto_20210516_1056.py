# Generated by Django 3.1.7 on 2021-05-16 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0010_question_success_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='field_type',
            field=models.CharField(choices=[('TX', 'Long multiline Text input'), ('SO', 'Pick one of multiple options'), ('MO', 'Pick several of multiple options'), ('SL', 'Short single line text input'), ('FU', 'File Upload'), ('DT', 'Date')], default='SO', max_length=2),
        ),
    ]