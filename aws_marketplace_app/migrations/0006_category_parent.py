# Generated by Django 3.2.9 on 2021-11-24 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aws_marketplace_app', '0005_posting_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aws_marketplace_app.category'),
        ),
    ]