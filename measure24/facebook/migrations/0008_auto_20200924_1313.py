# Generated by Django 2.2.6 on 2020-09-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0007_auto_20200209_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookpost',
            name='date',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
