# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from home import views


urlpatterns = [
    url(r'^$',views.IndexView.as_view(), name='index'),
    url(r'^features/$', views.FeatureView.as_view(), name='features'),
    url(r'^upload/$', views.model_form_upload, name='model_form_upload'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^analyze/$', views.AnalyzeView.as_view(), name='analyze'),
    url(r'^report/(?P<report_id>\d+)',views.report, name='report'),
    url(r'^parse_data/', views.parse_data, name='parse_data')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)