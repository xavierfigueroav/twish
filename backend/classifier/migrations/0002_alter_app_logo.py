# Generated by Django 3.2 on 2021-04-28 07:03
import classifier.models
import classifier.storage
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='logo',
            field=models.ImageField(blank=True, null=True, storage=classifier.storage.OverwriteableStorage, upload_to=classifier.models.logo_filename),
        ),
    ]
