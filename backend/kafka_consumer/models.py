from django.db import models
from django.db import models
from django.utils import timezone
import pickle
from django.contrib.postgres.fields import JSONField
from common.states import PENDING
from datetime import *
from common.states import UNKNOWN

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class LotModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False, max_length=200)


class ParkingSpotModel(models.Model):
    id = models.AutoField(primary_key=True)
    lot = models.ForeignKey(LotModel, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True, blank=True)
    coordinates = JSONField(default=list)
    status = models.IntegerField(default=PENDING)
    ttl = models.FloatField(default=0.0)

class SpotHistoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ParkingSpotModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    occupancy = models.IntegerField(default=UNKNOWN)

class LotHistoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    lot = models.ForeignKey(LotModel, on_delete=models.CASCADE)
    num_vacant = models.IntegerField(default=0)
    num_occupied = models.IntegerField(default=0)
    num_unknown = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)





class SpotterModel(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    image = models.BinaryField(default=pickle.dumps(None))
    image_file = models.FileField(blank=False, null=False, upload_to="lot_images/", default="")
    rects = JSONField()
    lot_id = models.ForeignKey(LotModel, on_delete=models.CASCADE)


class LotStateModel(models.Model):
    id = models.AutoField(primary_key=True)
    full_spots = models.IntegerField()
    available_spots = models.IntegerField()
    timestamp = models.DateTimeField()
    rects = JSONField()
    lot_id = models.ForeignKey(LotModel, on_delete=models.CASCADE)


class SettingsModel(models.Model):
    id = models.AutoField(primary_key=True)
    lot = models.ForeignKey(LotModel, on_delete=models.CASCADE)
    ttl_to_accept = models.IntegerField(default=30, null=False, blank=False)
