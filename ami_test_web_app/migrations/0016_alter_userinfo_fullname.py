# Generated by Django 4.2.3 on 2023-08-28 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ami_test_web_app', '0015_remove_userinfo_firstname_remove_userinfo_lastname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='fullname',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
