from django.contrib import admin

# Register your models here.
from .models import LotStateModel, LotModel, SpotterModel

admin.site.register(LotModel)
admin.site.register(LotStateModel)
admin.site.register(SpotterModel)