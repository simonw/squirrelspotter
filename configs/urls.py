from django.conf.urls import patterns, url #, include

urlpatterns = patterns('',
    url(r'^spot/(\d+)/$', 'spots.views.spot'),
    url(r'^robots\.txt$', 'spots.views.robots_txt'),
)
