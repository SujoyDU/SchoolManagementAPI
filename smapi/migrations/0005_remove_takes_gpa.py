# Generated by Django 3.1.2 on 2020-10-14 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0004_remove_takes_take_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takes',
            name='gpa',
        ),
    ]