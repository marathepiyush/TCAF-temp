# Generated by Django 4.1.7 on 2023-06-01 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ami_test_web_app', '0005_auto_20230519_1855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='fullname',
            new_name='firstname',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='lastname',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='middlename',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='role',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
