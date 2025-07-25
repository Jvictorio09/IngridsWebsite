# Generated by Django 5.1.2 on 2025-06-17 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pdf_link',
            field=models.URLField(blank=True, help_text='Public Google Drive link to product PDF', null=True),
        ),
    ]
