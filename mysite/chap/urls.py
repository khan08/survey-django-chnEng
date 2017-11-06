from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.InterviewIndexView.as_view(), name='interview'),
    url(r'^(?P<interview_id>[0-9]+)/instrument/(?P<instrument_id>[0-9]+)/$', views.questionView, name='interview'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)