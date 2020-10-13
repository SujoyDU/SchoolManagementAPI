# Generated by Django 3.1.2 on 2020-10-13 03:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapi', '0013_auto_20201008_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sid', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('total_credit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('dept_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='studept', to='smapi.department')),
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]