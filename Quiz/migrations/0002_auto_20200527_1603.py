# Generated by Django 3.0.6 on 2020-05-27 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Question', '0002_auto_20200527_1603'),
        ('User', '0001_initial'),
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='quiz_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Teacher'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='quiz_class_room',
            field=models.ManyToManyField(to='User.ClassRoom'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='quiz_questions',
            field=models.ManyToManyField(to='Question.Question'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='quiz_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Subject'),
        ),
        migrations.AddField(
            model_name='answers',
            name='amswers_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answers', to='User.Student'),
        ),
        migrations.AddField(
            model_name='answers',
            name='answer_class_room',
            field=models.ManyToManyField(to='User.ClassRoom'),
        ),
        migrations.AddField(
            model_name='answers',
            name='answer_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Subject'),
        ),
        migrations.AddField(
            model_name='answers',
            name='answers_questions',
            field=models.ManyToManyField(to='Question.Question'),
        ),
        migrations.AddField(
            model_name='answers',
            name='answers_quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quiz.Quiz'),
        ),
    ]
