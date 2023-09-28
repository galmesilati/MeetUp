# Generated by Django 4.2.1 on 2023-09-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kidmeet_app', '0012_alter_child_events_alter_event_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='day_of_week',
            field=models.CharField(choices=[('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')], default='tuesday', max_length=10),
        ),
    ]
