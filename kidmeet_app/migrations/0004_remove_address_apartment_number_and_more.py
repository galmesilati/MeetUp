# Generated by Django 4.2.1 on 2023-06-26 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kidmeet_app', '0003_alter_child_age_alter_child_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='apartment_number',
        ),
        migrations.RemoveField(
            model_name='address',
            name='building_number',
        ),
        migrations.AddField(
            model_name='address',
            name='house_number',
            field=models.CharField(db_column='house_number', default=0, max_length=20),
            preserve_default=False,
        ),
    ]
