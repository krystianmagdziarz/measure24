# Generated by Django 2.2.6 on 2020-01-28 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='words',
            options={'verbose_name': 'Monitorowane słowo', 'verbose_name_plural': 'Monitorowane słowa'},
        ),
    ]
