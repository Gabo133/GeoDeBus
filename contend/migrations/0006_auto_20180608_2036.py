# Generated by Django 2.0.6 on 2018-06-08 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contend', '0005_auto_20180608_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gps',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='gps',
            name='lng',
            field=models.FloatField(default=0),
        ),
    ]
