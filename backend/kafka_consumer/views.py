from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .models import LotModel, LotStateModel, SpotterModel
from django.forms.models import model_to_dict
import base64
import pickle
# Create your views here.

def index(req):
    return HttpResponse("index")

def lot_list(req):
    obj = list(map(lambda x: model_to_dict(x), LotModel.objects.all()))

    return JsonResponse(obj, safe=False)

def lot_detail(req, id):
    obj = LotModel.objects.get(id=id)
    return JsonResponse(model_to_dict(obj), safe=False)

def lot_info(req,id):
    lot = LotModel.objects.get(id=id)
    lot_info = list(map(lambda x: model_to_dict(x), LotStateModel.objects.filter(lot_id=lot)))
    return JsonResponse(lot_info, safe=False)

def lot_rects(req, id):
    lot_rects = SpotterModel.objects.get(lot_id=id)
    return JsonResponse(model_to_dict(lot_rects), safe=False)

def lot_image(req, id):
    lot_rects = SpotterModel.objects.get(lot_id=id)
    b64_image = base64.b64encode(lot_rects.image).decode("ascii")
    return HttpResponse("data:image/jpeg;base64,"+b64_image)