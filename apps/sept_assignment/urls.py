from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'(?P<poke_target_id>\d+)$', views.poke, name = 'poke')
]
