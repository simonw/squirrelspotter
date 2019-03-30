from django.contrib import admin
from django.urls import re_path
from django.conf import settings

import spotter.views

urlpatterns = [
    re_path(r'^$', spotter.views.index),
    re_path(r'^login/$', spotter.views.login),
    re_path(r'^login2/$', spotter.views.login2),
    re_path(r'^debug/$', spotter.views.debug),
    re_path(r'^scores/$', spotter.views.scores),
    re_path(r'^login/done/$', spotter.views.done),
    re_path(r'^logout/$', spotter.views.logout),

    re_path(r'^spot/(\d+)/$', spotter.views.spot),
    re_path(r'^spotted/$', spotter.views.spotted),

    re_path(r'^twilio/sms/$', spotter.views.twilio_sms),

    re_path(r'^robots\.txt$', spotter.views.robots_txt),
    re_path(r'^channel\.html$', spotter.views.channel_html),
    # path(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
    #     'document_root': settings.STATIC_ROOT
    # }),
]

