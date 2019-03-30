from django.shortcuts import render as render_original
from django.template import RequestContext
from django.conf import settings

def render(request, template, context = None, content_type=None):
    context = context or {}
    context['app_id'] = settings.FB_APP_ID
    context['forced_logged_out'] = request.COOKIES.get('logged_out')
    return render_original(request, template, context, content_type=content_type)
