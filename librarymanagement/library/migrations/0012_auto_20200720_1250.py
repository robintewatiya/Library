# Generated by Django 3.0.7 on 2020-07-20 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_pendingaddrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
