from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class DetectorResult(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = AutoDateTimeField()
    rects = JSONField()
    lot_id = models.IntegerField()

