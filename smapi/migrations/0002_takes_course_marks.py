# Generated by Django 3.1.2 on 2020-10-18 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='takes',
            name='course_marks',
            field=models.FloatField(default=-1),
        ),
    ]
