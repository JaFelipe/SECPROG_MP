# Generated by Django 2.1.7 on 2019-03-11 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20190311_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='locNumber',
            new_name='location',
        ),
    ]
