# Generated by Django 2.2.10 on 2020-03-29 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kafka_consumer', '0017_auto_20200324_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotmodel',
            name='video_src',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='lothistorymodel',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='kafka_consumer.LotModel'),
        ),
        migrations.AlterField(
            model_name='spothistorymodel',
            name='spot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='kafka_consumer.ParkingSpotModel'),
        ),
    ]
