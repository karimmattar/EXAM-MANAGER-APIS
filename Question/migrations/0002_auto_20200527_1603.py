# Generated by Django 3.0.6 on 2020-05-27 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
        ('Question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Teacher'),
        ),
        migrations.AddField(
            model_name='rate',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Question.Question'),
        ),
        migrations.AddField(
            model_name='rate',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Teacher'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Subject'),
        ),
        migrations.AddField(
            model_name='mcq',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Question.Question'),
        ),
    ]