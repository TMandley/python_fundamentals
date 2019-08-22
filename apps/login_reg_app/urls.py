from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^regvalidate$', views.regvalidate),
    url(r'^logvalidate$', views.logvalidate),
    url(r'^success/(?P<num>\d+)$', views.success),
    url(r'^destroy$', views.destroy),
    url(r'^regfnvalidate$', views.regfnvalidate),
    url(r'^reglnvalidate$', views.reglnvalidate),
    url(r'', views.index),
]