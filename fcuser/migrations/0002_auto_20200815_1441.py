# Generated by Django 3.1 on 2020-08-15 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fcuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fcuser',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자'},
        ),
        migrations.AlterModelTable(
            name='fcuser',
            table='fastcampus_fcuser',
        ),
    ]
