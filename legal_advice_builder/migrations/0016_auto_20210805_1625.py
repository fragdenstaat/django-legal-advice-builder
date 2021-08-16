# Generated by Django 3.1.7 on 2021-08-05 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legal_advice_builder', '0015_textblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='condition',
            options={'default_related_name': 'question_condition'},
        ),
        migrations.AlterField(
            model_name='condition',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_condition', to='legal_advice_builder.question'),
        ),
        migrations.AlterField(
            model_name='condition',
            name='then_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='then_question_conditions', to='legal_advice_builder.question'),
        ),
        migrations.CreateModel(
            name='TextBlockCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_option', models.CharField(max_length=500)),
                ('if_value', models.CharField(max_length=500)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_block_condition', to='legal_advice_builder.question')),
                ('text_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_block_conditions', to='legal_advice_builder.textblock')),
            ],
            options={
                'default_related_name': 'text_block_condition',
                'unique_together': {('question', 'if_value')},
            },
        ),
    ]