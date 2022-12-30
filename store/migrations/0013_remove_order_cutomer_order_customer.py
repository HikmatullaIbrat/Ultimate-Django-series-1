# Generated by Django 4.1.2 on 2022-12-30 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_order_cutomer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cutomer',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=1000, on_delete=django.db.models.deletion.PROTECT, to='store.customer', verbose_name='order of customer'),
            preserve_default=False,
        ),
    ]
