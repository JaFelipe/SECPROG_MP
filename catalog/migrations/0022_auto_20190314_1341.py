# Generated by Django 2.1.5 on 2019-03-14 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_roominstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roominstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set room as returned'),)},
        ),
        migrations.AddField(
            model_name='roominstance',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Room'),
        ),
    ]