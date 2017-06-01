from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^travels', views.home, name="home"),
    url(r'^destination/(?P<id>\d*)', views.destination, name='destination'),
    url(r'^jointrip/(?P<id>\d*)', views.jointrip, name="jointrip"),
    url(r'^add', views.add, name="add"),
    url(r'^post', views.post, name="post")
]
