# Generated by Django 3.1.2 on 2020-10-21 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='exam', to='smapi.teaches'),
        ),
        migrations.AlterField(
            model_name='giveexam',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='takesstudent', to='smapi.takes'),
        ),
    ]