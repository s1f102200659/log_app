# Generated by Django 5.0.7 on 2024-09-08 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('garden_id', models.AutoField(primary_key=True, serialize=False)),
                ('postal_code', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=128)),
                ('policy', models.TextField()),
                ('garden_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Caretaker',
            fields=[
                ('caretaker_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('grade', models.IntegerField()),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caretakers', to='log_app.garden')),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('journal_id', models.AutoField(primary_key=True, serialize=False)),
                ('grade', models.IntegerField()),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='log_app.garden')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=100)),
                ('grade', models.IntegerField()),
                ('student_info', models.TextField()),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='log_app.garden')),
            ],
        ),
        migrations.CreateModel(
            name='StudentJournal',
            fields=[
                ('studentjournal_id', models.AutoField(primary_key=True, serialize=False)),
                ('journal_info', models.TextField()),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentjournals', to='log_app.student')),
            ],
        ),
    ]
