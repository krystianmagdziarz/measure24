# Generated by Django 2.2.6 on 2020-02-09 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0006_auto_20200128_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookgroup',
            name='facebook_user',
            field=models.ForeignKey(help_text='Użytkownik z prawem dostępu do grupy', on_delete=django.db.models.deletion.CASCADE, to='facebook.FacebookUser'),
        ),
        migrations.AlterField(
            model_name='facebookgroup',
            name='name',
            field=models.CharField(blank=True, help_text='Nazwa w systemie', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facebookgroup',
            name='permalink',
            field=models.CharField(help_text='Adres lub ID grupy', max_length=256),
        ),
    ]