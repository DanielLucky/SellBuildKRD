from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    # url('register/', views.registerPage, name='register'),
    # url('login1/', views.loginPage, name='login'),
    # url('logout/', views.logoutUser, name='logout'),
    url('contact/', views.ContactSendView, name='contact'),
    url('submit/', views.submitSell, name='submit'),
    url('detail/', views.agencyDetail, name='agencyDetail'),
    path("signup/", views.SignUp.as_view(), name="signup")
]
