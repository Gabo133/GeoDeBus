# Generated by Django 2.0.6 on 2018-06-11 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contend', '0011_auto_20180611_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
