# Generated by Django 3.2.9 on 2021-11-19 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(max_length=256)),
                ('postal_code', models.IntegerField()),
                ('manufacturer', models.CharField(max_length=256)),
                ('model_name', models.CharField(max_length=256)),
                ('length_cm', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width_cm', models.DecimalField(decimal_places=2, max_digits=10)),
                ('height_cm', models.DecimalField(decimal_places=2, max_digits=10)),
                ('condition', models.IntegerField(choices=[(None, '(Unknown)'), (1, 'New'), (2, 'Used - Like New'), (3, 'Used - Excellent'), (4, 'Used - Good'), (5, 'Used - Fair'), (6, 'Used - Salvage')])),
                ('can_meetup', models.BooleanField(default=True)),
                ('can_deliver', models.BooleanField(default=False)),
                ('is_draft', models.BooleanField(default=True)),
                ('is_reserved', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aws_marketplace_app.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posting_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posting_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posting_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]