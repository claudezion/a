# Generated by Django 5.1.1 on 2024-10-04 11:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admin_panel", "0002_user_country_user_dob_user_mobile_user_profile_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Referral",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "referred_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referrals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "referred_user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="referred",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
