# Generated by Django 4.2.11 on 2025-03-10 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2, help_text="Price in EUR (€)", max_digits=10
            ),
        ),
    ]
