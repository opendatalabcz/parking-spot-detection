# Generated by Django 2.2.10 on 2020-03-24 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka_consumer', '0011_auto_20200324_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spothistorymodel',
            name='status',
            field=models.IntegerField(default=-1),
        ),
    ]