from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)/(?P<participant_id>[0-9]+)/$', views.InterviewIndexView.as_view(), name='interview'),
    url(r'^(?P<interview_id>[0-9]+)/(?P<participant_id>[0-9]+)/instrument/(?P<instrument_id>[0-9]+)/$', views.questionView, name='interview'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)