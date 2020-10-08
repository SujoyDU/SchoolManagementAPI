# Generated by Django 3.1.2 on 2020-10-08 00:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0010_instructor_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='dept_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='smapi.department'),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='salary',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(29000), django.core.validators.MaxValueValidator(300000)]),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='uid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='instructor', to=settings.AUTH_USER_MODEL),
        ),
    ]
