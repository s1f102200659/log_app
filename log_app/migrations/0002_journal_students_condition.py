# Generated by Django 5.1.1 on 2024-10-25 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='students_condition',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]