# Generated by Django 4.2.20 on 2025-03-14 16:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("funding", "0002_rename_profile_users"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Users",
            new_name="User",
        ),
    ]
