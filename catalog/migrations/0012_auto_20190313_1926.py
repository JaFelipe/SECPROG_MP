# Generated by Django 2.1.7 on 2019-03-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20190312_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='color',
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.CharField(default='Tag', help_text='Tags', max_length=10),
        ),
    ]
