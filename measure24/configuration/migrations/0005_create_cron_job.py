import os
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0004_configuration_max_entry'),
    ]

    def create_cron_job(apps, schema_editor):
        from chroniker.models import Job

        job = Job()
        job.name = "Monitoring grup"
        job.frequency = "MINUTELY"
        job.params = "interval: 3"
        job.command = "get_facebook"
        job.enabled = True
        job.email_errors_to_subscribers = False
        job.save()

    operations = [
        migrations.RunPython(create_cron_job),
    ]
