from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    # /api/lot
    path('lot/', views.lot, name='lot_detail'),
    path('lot/<int:id>/', views.lot, name='lot_detail'),
    path('lot/<int:id>/settings/', views.lot_settings, name='lot_settings'),
    path('lot/<int:id>/snapshot/', views.snapshot_stream, name='lot_settings'),
    # /api/lot/history
    path('lot/<int:id>/history/', views.lot_history, name="lot_history"),
    # /api/spot
    path('lot/<int:lot_id>/spot/', views.lot_spot, name="lot_spots"),
    path('lot/<int:lot_id>/spot/<int:spot_id>/', views.lot_spot, name="lot_spots"),
    # /api/spot/history
    path('lot/<int:lot_id>/spot/<int:spot_id>/history/', views.lot_spot_history, name="lot_spots")
    # POST /api/lot/spots/

]
