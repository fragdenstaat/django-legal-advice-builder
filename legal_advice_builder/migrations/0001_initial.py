# Generated by Django 3.1.7 on 2021-08-25 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sample_answers', models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LawCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('allow_download', models.BooleanField(default=True)),
                ('save_answers', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('document', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='legal_advice_builder.document')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('short_title', models.CharField(blank=True, max_length=50)),
                ('text', models.CharField(max_length=200)),
                ('options', models.JSONField(blank=True, default=dict, null=True)),
                ('field_type', models.CharField(choices=[('TX', 'Long multiline Text input'), ('SO', 'Pick one of multiple options'), ('SL', 'Short single line text input'), ('DT', 'Date'), ('YN', 'Yes/No')], default='SO', max_length=2)),
                ('help_text', models.CharField(blank=True, max_length=200)),
                ('information', models.TextField(blank=True)),
                ('is_last', models.BooleanField(default=False)),
                ('next_question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='legal_advice_builder.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('content', models.TextField(default='')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_text_blocks', to='legal_advice_builder.document')),
            ],
            options={
                'ordering': ['order'],
            },
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
            },
        ),
        migrations.CreateModel(
            name='Questionaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('short_title', models.CharField(blank=True, max_length=50)),
                ('success_message', models.TextField(blank=True, default='your message here ...', help_text='This message is shown if the user has answered all questions successfully.')),
                ('unsure_message', models.TextField(blank=True)),
                ('order', models.IntegerField()),
                ('law_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legal_advice_builder.lawcase')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='questionaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='legal_advice_builder.questionaire'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.JSONField(blank=True, default=dict, null=True)),
                ('rendered_document', models.TextField(blank=True, verbose_name='Rendered Document')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('law_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legal_advice_builder.lawcase')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('if_option', models.CharField(max_length=500)),
                ('if_value', models.CharField(max_length=500)),
                ('then_value', models.CharField(max_length=500)),
                ('message', models.TextField(blank=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_condition', to='legal_advice_builder.question')),
                ('then_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='then_question_conditions', to='legal_advice_builder.question')),
            ],
            options={
                'default_related_name': 'question_condition',
                'unique_together': {('question', 'if_value', 'then_value')},
            },
        ),
    ]
