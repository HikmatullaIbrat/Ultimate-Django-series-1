# Generated by Django 4.1.2 on 2022-12-29 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_product_membership_choice_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='unit_price',
        ),
    ]