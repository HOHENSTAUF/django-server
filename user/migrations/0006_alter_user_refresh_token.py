# Generated by Django 5.0.4 on 2024-04-15 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_user_refresh_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="refresh_token",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
