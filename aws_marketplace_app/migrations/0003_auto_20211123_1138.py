# Generated by Django 3.2.9 on 2021-11-23 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aws_marketplace_app', '0002_auto_20211123_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posting_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posting',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posting_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]