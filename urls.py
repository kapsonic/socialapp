from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^admin', views.admin, name="admin"),
    url(r'^social', views.home, name="home"),
    url(r'^healthcare', views.healthCareHome, name="healthcare"),
    url(r'^chat', views.chat, name="chat"),
    url(r'^initSession', views.initSession, name="initSession"),
    url(r'^getCode', views.getCode, name="getCode"),
    url(r'^pollStatus', views.pollStatus, name="pollStatus"),
    url(r'^createChallenge', views.createChallenge, name="createChallenge")
]