# Generated by Django 5.1.5 on 2025-02-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movie', '0002_rename_directory_moviedirectory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedirectory',
            name='duration',
            field=models.CharField(max_length=75),
        ),
    ]
