# Generated by Django 2.2.10 on 2020-03-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka_consumer', '0013_remove_spothistorymodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='spothistorymodel',
            name='status',
            field=models.IntegerField(default=-1),
        ),
    ]
