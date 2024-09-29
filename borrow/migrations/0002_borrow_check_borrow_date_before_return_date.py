# Generated by Django 5.1 on 2024-09-04 17:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
        ("borrow", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="borrow",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("borrow_date__lte", models.F("expected_return_date"))
                ),
                name="check_borrow_date_before_return_date",
            ),
        ),
    ]
