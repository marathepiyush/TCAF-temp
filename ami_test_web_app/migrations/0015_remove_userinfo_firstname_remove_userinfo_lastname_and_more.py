# Generated by Django 4.2.3 on 2023-08-28 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ami_test_web_app', '0014_projectorgchoices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='middlename',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='fullname',
            field=models.CharField(default='default name given', max_length=100),
        ),
    ]