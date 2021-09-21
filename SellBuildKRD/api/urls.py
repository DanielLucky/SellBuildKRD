from django.urls import path
from . import views


urlpatterns = [
    path("v1/sell/add", views.get_sell),
    path("v1/sell/all", views.Sells_View.as_view()),
    path("v1/sell/<int:id_sell>", views.get_sell),
    path("v1/sell/delete/<int:id_sell>", views.delete_sell),
]

