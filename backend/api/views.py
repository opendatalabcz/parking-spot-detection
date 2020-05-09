from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpResponseBadRequest
from kafka_consumer.models import LotModel , LotHistoryModel, ParkingSpotModel, SpotHistoryModel, SettingsModel
import cv2
from PIL import Image, ImageDraw
from django.forms.models import model_to_dict
import base64
from django.core import serializers as s
import json
import pickle
import datetime
from django.core.files.storage import FileSystemStorage
from common.states import ACCEPTED, PENDING, BLOCKER
from django.views.decorators.csrf import csrf_exempt
from common.common_utils import timed
from common.producers import MessageProducer
from common.messages import SlicerMessage
from common.topics import TOPIC_SLICE
def index(req):
    return HttpResponse("index")

@csrf_exempt
def lot(request, id=None):

    if request.method == "POST" and not id:
        data = request.POST.get("data", [])
        if data:
            data = json.loads(data)
            obj = LotModel(name=data["name"])
            obj.save()
            settings = SettingsModel(lot=obj, video_src=data['video_src'])
            settings.save()
            id = obj.id


    if not id:
        lots = list(LotModel.objects.all().values('id', 'name'))
        for lot in lots:
            last_history = LotHistoryModel.objects\
                .filter(lot_id=lot["id"]).order_by('-timestamp')\
                .values('timestamp','num_occupied', 'num_vacant', 'num_unknown')

            if last_history:
                lot.update(last_history[0])

        return JsonResponse(lots, safe=False)

    else:
        response = dict(LotModel.objects.filter(id=id)
                        .prefetch_related('history')
                        .order_by('-history__timestamp')
                        .values('name', 'history__id', 'history__timestamp', 'history__num_occupied',
                                'history__num_vacant', 'history__num_unknown')[0])
    return JsonResponse(response, safe=False)


def lot_history(request, id):
    response = list(LotHistoryModel.objects.filter(lot_id=id).values('timestamp','num_occupied', 'num_vacant', 'num_unknown'))
    return JsonResponse(response, safe=False)


@csrf_exempt
def lot_spot(request, lot_id, spot_id=None):

    if request.method == "POST":
        data = request.POST.get("data", [])
        print(data)
        if data:
            data = json.loads(data)
            all_spots = list(ParkingSpotModel.objects.all())

            for item in data:
                if item["id"] != -1:
                    obj = ParkingSpotModel.objects.get(id=item["id"])
                    obj.coordinates = item["coordinates"]
                    obj.status = item["status"]
                else:
                    obj = ParkingSpotModel(lot_id=lot_id, coordinates=item["coordinates"], status=item["status"])
                obj.save()

            incoming_ids = list(map(lambda x: x["id"], data))
            print(incoming_ids)

            for spot in all_spots:
                if spot.id not in incoming_ids:
                    spot.delete()

    if not spot_id:
        response = list(ParkingSpotModel.objects.filter(lot_id=lot_id, status__in=[ACCEPTED, PENDING, BLOCKER]).values('id', 'coordinates', 'status'))
    else:
        response = dict(ParkingSpotModel.objects.filter(lot_id=lot_id, id=spot_id, status__in=[ACCEPTED, PENDING, BLOCKER]).values('id', 'coordinates', 'status')[0])
    return JsonResponse(response, safe=False)


def lot_spot_history(request, lot_id, spot_id):
    spot = ParkingSpotModel.objects.filter(lot_id=lot_id, id=spot_id)[0]
    response = list(SpotHistoryModel.objects.filter(spot_id=spot.id).values('timestamp', 'occupancy'))

    return JsonResponse(response, safe=False)

@csrf_exempt
def lot_settings(request, id):
    settings = SettingsModel.objects.get(lot_id=id)
    if request.method == "POST":
        data = request.POST.get("data", [])
        if data:
            data = json.loads(data)
            print(data)
            settings = SettingsModel.objects.get(lot_id=id)
            settings.video_src = data['video_src']
            settings.ttl_to_accept = data['ttl']
            settings.running = data['detection_running']
            settings.save()

    return JsonResponse(model_to_dict(settings), safe=False)

def snapshot_stream(request, id):

    def write_not_working(img):
        draw = ImageDraw.Draw(img)
        draw.text((95, 145), "Stream not working", fill="white")

    def write_date_time(img):
        draw = ImageDraw.Draw(img)
        draw.text((10,10), str(datetime.datetime.now()), fill="white", stroke_width=1, stroke_fill="black")

    try:
        settings = SettingsModel.objects.get(lot_id=id)

        cap = cv2.VideoCapture(settings.video_src, cv2.CAP_FFMPEG)
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame, 'RGB')
        write_date_time(img)
        response = HttpResponse(content_type="image/jpeg")
        img.save(response, "JPEG")
        return response
    except Exception as e:
        img = Image.new("RGB", (300,300))
        response = HttpResponse(content_type="image/jpeg")
        write_not_working(img)
        img.save(response, "JPEG")
        return response
