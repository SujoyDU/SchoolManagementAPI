# Generated by Django 3.1.2 on 2020-10-20 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0008_auto_20201019_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giveexam',
            name='stuexam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuexam', to='smapi.exam'),
        ),
    ]
