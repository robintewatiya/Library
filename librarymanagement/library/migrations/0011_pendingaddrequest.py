# Generated by Django 2.1.4 on 2020-07-18 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_book_allotment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingAddRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.PositiveIntegerField()),
                ('user_id', models.PositiveIntegerField()),
            ],
        ),
    ]
