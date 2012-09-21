from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'spotter.views.index'),
    url(r'^login/$', 'spotter.views.login'),
    url(r'^debug/$', 'spotter.views.debug'),
    url(r'^scores/$', 'spotter.views.scores'),
    url(r'^login/done/$', 'spotter.views.done'),
    url(r'^spot/(\d+)/$', 'spotter.views.spot'),
    url(r'^spotted/$', 'spotter.views.spotted'),
    url(r'^robots\.txt$', 'spotter.views.robots_txt'),
    url(r'^channel\.html$', 'spotter.views.channel_html'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),

    (r'^admin-peeps/', include(admin.site.urls)),
)
