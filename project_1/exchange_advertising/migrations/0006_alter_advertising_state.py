# Generated by Django 4.1 on 2022-11-25 07:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_advertising", "0005_alter_advertising_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertising",
            name="state",
            field=models.IntegerField(
                default=2,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(3),
                ],
            ),
        ),
    ]