# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from home import views


urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^analyze/$', views.analyze, name='analyze'),
    url(r'^report/(?P<report_id>\d+)',views.report, name='report'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)