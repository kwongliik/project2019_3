# Generated by Django 2.1.7 on 2019-04-11 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventori', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stok',
            name='starter',
        ),
    ]
