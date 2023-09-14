# Generated by Django 4.2.1 on 2023-07-13 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kidmeet_app', '0007_rename_place_event_location_alter_event_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='end_time',
            new_name='end_event',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start_time',
            new_name='start_event',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='day_of_week',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='start_time',
        ),
    ]
