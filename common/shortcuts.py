from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def render(request, template, context = None, content_type=None):
    context = context or {}
    context['app_id'] = settings.FB_APP_ID
    context['forced_logged_out'] = request.COOKIES.get('logged_out')
    return render_to_response(
        template, context,
        context_instance = RequestContext(request, context),
        mimetype=content_type,
    )
