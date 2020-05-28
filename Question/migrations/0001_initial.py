# Generated by Django 3.0.6 on 2020-05-27 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MCQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_head', models.CharField(blank=True, max_length=255, null=True)),
                ('question_head_avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('question_body', models.CharField(max_length=250)),
                ('choice_A', models.CharField(max_length=100)),
                ('choice_B', models.CharField(max_length=100)),
                ('choice_C', models.CharField(max_length=100)),
                ('choice_D', models.CharField(max_length=100)),
                ('question_answer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('question_type', models.CharField(max_length=50)),
                ('question_creation_time', models.DateTimeField(auto_now_add=True)),
                ('question_real_time', models.IntegerField()),
                ('question_customization_time', models.IntegerField()),
                ('question_points', models.IntegerField(default=1)),
                ('question_grade', models.CharField(max_length=50)),
                ('question_level', models.CharField(max_length=50)),
                ('question_topic', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.CharField(max_length=10)),
                ('comment', models.CharField(blank=True, max_length=250, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_body', models.CharField(max_length=250)),
                ('question_answer', models.CharField(max_length=100)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Question.Question')),
            ],
        ),
    ]