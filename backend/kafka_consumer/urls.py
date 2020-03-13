from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('lot/', views.lot_list, name='lot_list'),
    path('lot/<int:id>/', views.lot_detail, name='lot_detail'),
    path('lot_info/<int:id>/', views.lot_info, name='lot_info'),
    path('lot_rects/<int:id>/', views.lot_rects, name='lot_rects'),
    path('lot_image/<int:id>/', views.lot_image, name='lot_image'),
]
