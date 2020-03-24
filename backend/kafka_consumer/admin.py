from django.contrib import admin

# Register your models here.
from .models import ParkingSpotModel, LotModel, SpotHistoryModel

admin.site.register(LotModel)
admin.site.register(ParkingSpotModel)
admin.site.register(SpotHistoryModel)