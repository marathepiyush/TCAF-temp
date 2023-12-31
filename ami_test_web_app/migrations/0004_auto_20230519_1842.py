# Generated by Django 3.2.19 on 2023-05-19 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ami_test_web_app', '0003_merge_20230518_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='dimensions',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usercategories',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Initiatives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initiative_type', models.CharField(max_length=50, unique=True)),
                ('initiative', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('tieBackToCurrentStateFindings', models.CharField(max_length=500)),
                ('complexity', models.CharField(max_length=20)),
                ('parameter', models.CharField(max_length=50)),
                ('specification', models.CharField(max_length=50)),
                ('condition', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ami_test_web_app.categories')),
                ('dimension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ami_test_web_app.dimensions')),
            ],
            options={
                'db_table': 'initiatives',
            },
        ),
    ]
