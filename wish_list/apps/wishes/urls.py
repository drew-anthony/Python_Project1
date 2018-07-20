from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^registration$', views.registration),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^itemCreate$', views.itemCreate),
    url(r'^wish_items$', views.wish_items),
    url(r'^remove$', views.remove),
    url(r'^delete$', views.delete),
    

]    