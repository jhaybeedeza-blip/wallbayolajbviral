# Generated migration for adding music snippet selection fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_add_ghost_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='unsentmessage',
            name='music_start_time',
            field=models.FloatField(blank=True, default=0, help_text='Song snippet start time in seconds', null=True),
        ),
        migrations.AddField(
            model_name='unsentmessage',
            name='music_end_time',
            field=models.FloatField(blank=True, help_text='Song snippet end time in seconds', null=True),
        ),
    ]
