from django.conf.urls import patterns, url #, include
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'spotter.views.index'),
    url(r'^login/$', 'spotter.views.login'),
    url(r'^login/done/$', 'spotter.views.done'),
    url(r'^spot/(\d+)/$', 'spotter.views.spot'),
    url(r'^robots\.txt$', 'spotter.views.robots_txt'),
    url(r'^channel\.html$', 'spotter.views.channel_html'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)
