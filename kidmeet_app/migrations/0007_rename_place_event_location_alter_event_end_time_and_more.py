# Generated by Django 4.2.1 on 2023-07-06 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kidmeet_app', '0006_alter_userdetails_address_alter_userdetails_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='place',
            new_name='location',
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(db_column='end_event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(db_column='start_event'),
        ),
    ]
