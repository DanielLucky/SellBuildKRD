import django
from django.conf.urls import url
from . import views


urlpatterns = [
    url('register/', views.registerPage, name='register'),
    url('login/', views.loginPage, name='login'),
    url('logout/', views.logoutUser, name='logout'),
    url('submit/', views.submitSell, name='submit'),
    url('detail/', views.agencyDetail, name='agencyDetail'),

]
