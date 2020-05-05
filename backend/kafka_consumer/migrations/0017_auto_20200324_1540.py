# Generated by Django 2.2.10 on 2020-03-24 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kafka_consumer', '0016_auto_20200324_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='spothistorymodel',
            name='occupancy',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='spothistorymodel',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='LotHistoryModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num_vacant', models.IntegerField(default=0)),
                ('num_occupied', models.IntegerField(default=0)),
                ('num_unknown', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kafka_consumer.LotModel')),
            ],
        ),
    ]
