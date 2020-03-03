from django.db import models
from django.db import models
from django.utils import timezone
import pickle
from django.contrib.postgres.fields import JSONField

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class LotModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False, max_length=200)


class SpotterModel(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    image = models.BinaryField(default=pickle.dumps(None))
    rects = JSONField()
    lot_id = models.ForeignKey(LotModel, on_delete=models.CASCADE)



class LotStateModel(models.Model):
    id = models.AutoField(primary_key=True)
    full_spots = models.IntegerField()
    available_spots = models.IntegerField()
    timestamp = models.DateTimeField()
    lot_id = models.ForeignKey(LotModel, on_delete=models.CASCADE)
