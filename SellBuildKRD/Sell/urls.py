from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/v1/sell/add", views.get_sell),
    path("api/v1/sell/<int:id_sell>", views.get_sell),
    path("<int:id_item>", views.sell),
]


