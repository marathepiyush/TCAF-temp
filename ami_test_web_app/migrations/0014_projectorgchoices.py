# Generated by Django 4.2.3 on 2023-07-25 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ami_test_web_app', '0013_alter_userinfo_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectOrgChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('response', models.TextField()),
            ],
        ),
    ]
