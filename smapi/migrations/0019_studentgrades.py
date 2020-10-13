# Generated by Django 3.1.2 on 2020-10-13 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0018_auto_20201013_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='smapi.course')),
                ('students', models.ManyToManyField(related_name='takes', to='smapi.Takes')),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teach', to='smapi.teaches')),
            ],
        ),
    ]
