# Generated by Django 4.1.2 on 2022-12-04 17:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggeditem',
            name='content_type',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taggeditem',
            name='object_id',
            field=models.PositiveIntegerField(default=3),
            preserve_default=False,
        ),
    ]
