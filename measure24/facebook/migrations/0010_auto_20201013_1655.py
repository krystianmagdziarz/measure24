# Generated by Django 2.2.6 on 2020-10-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0009_auto_20200924_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpostcommentlvl0',
            name='permalink',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facebookpostcommentlvl1',
            name='permalink',
            field=models.TextField(blank=True, null=True),
        ),
    ]
