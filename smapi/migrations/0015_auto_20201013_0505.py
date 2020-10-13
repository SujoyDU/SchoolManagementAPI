# Generated by Django 3.1.2 on 2020-10-13 05:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0014_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Takes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('Fa', 'Fall'), ('Su', 'Summer'), ('Wi', 'Winter'), ('Sp', 'Spring')], default='Fall', max_length=10)),
                ('year', models.DateField(null=True)),
                ('course_marks', models.PositiveIntegerField()),
                ('course_status', models.CharField(choices=[('C', 'Current'), ('F', 'FAIL'), ('P', 'PASS'), ('W', 'WITHDRAW'), ('T', 'TAKEN')], default='Current', max_length=10)),
                ('gpa', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='takescourse', to='smapi.course')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stu', to='smapi.student')),
            ],
        ),
        migrations.AddConstraint(
            model_name='takes',
            constraint=models.UniqueConstraint(fields=('course_id', 'semester', 'year'), name='unique_course_time'),
        ),
    ]
