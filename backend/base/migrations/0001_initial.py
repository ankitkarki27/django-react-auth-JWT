# Generated by Django 5.1.4 on 2024-12-25 19:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=225)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
