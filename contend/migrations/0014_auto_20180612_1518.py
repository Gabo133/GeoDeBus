# Generated by Django 2.0.6 on 2018-06-12 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contend', '0013_auto_20180612_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus',
            name='eliminado',
        ),
        migrations.RemoveField(
            model_name='ruta',
            name='eliminado',
        ),
    ]