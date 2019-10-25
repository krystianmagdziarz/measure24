# Generated by Django 2.2.6 on 2019-10-25 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('permalink', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='FacebookPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=32, unique=True)),
                ('author', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('permalink', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='FacebookPostCommentLvl0',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.CharField(max_length=32, unique=True)),
                ('author', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('link_profile', models.CharField(max_length=256)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.FacebookPost')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacebookPostCommentLvl1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.CharField(max_length=32, unique=True)),
                ('author', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('link_profile', models.CharField(max_length=256)),
                ('comment_lvl0', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facebook.FacebookPostCommentLvl0')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
