from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^regvalidate$', views.regvalidate),
    url(r'^logvalidate$', views.logvalidate),
    # url(r'^success/(?P<num>\d+)$', views.success),
    url(r'^jobs/new$', views.newjob),
    url(r'^jobs/edit/(?P<num>\d+)$', views.editjob),
    url(r'^jobs/(?P<num>\d+)$', views.jobinfo),
    url(r'^delete/(?P<num>\d+)$', views.deletejob),
    url(r'^giveup/(?P<num>\d+)$', views.giveup),
    url(r'^processnewjob$', views.processnewjob),
    url(r'^processaddjob/(?P<num>\d+)$', views.processaddjob),
    url(r'^processjobedit$', views.processjobedit),
    url(r'^dashboard$', views.success),
    url(r'^destroy$', views.destroy),
    url(r'^regfnvalidate$', views.regfnvalidate),
    url(r'^reglnvalidate$', views.reglnvalidate),
    url(r'', views.index),
]