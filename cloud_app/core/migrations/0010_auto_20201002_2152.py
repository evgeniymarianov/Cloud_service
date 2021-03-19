# Generated by Django 3.1 on 2020-10-02 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_additionalhdd_csv_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='current_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reports', to=settings.AUTH_USER_MODEL),
        ),
    ]