from django.conf.urls import patterns, url #, include

urlpatterns = patterns('',
    url(r'^$', 'spotter.views.index'),
    url(r'^spot/(\d+)/$', 'spotter.views.spot'),
    url(r'^robots\.txt$', 'spotter.views.robots_txt'),
    url(r'^channel\.html$', 'spotter.views.channel_html'),
)
