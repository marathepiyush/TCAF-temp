# Generated by Django 4.2.3 on 2023-09-18 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ami_test_web_app', '0019_initiativedetail_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='firstname',
            new_name='fullname',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='middlename',
        ),
    ]
