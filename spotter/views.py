from django.http import HttpResponse, HttpResponseRedirect
from common.shortcuts import render
from django.conf import settings
import urllib

def index(request):
    return render(request, 'index.html')

def spot(request, id):
    return HttpResponse("Spot %s" % id)

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow: /",
        content_type = 'text/plain'
    )

def channel_html(request):
    return HttpResponse('<script src="//connect.facebook.net/en_US/all.js"></script>')

def login(request):
    fb_login_uri = "https://www.facebook.com/dialog/oauth?" + urlib.urlencode({
        'client_id': settings.FB_APP_ID,
        'redirect_uri': 'http://thawing-earth-2731.herokuapp.com/login/done/',
        'scope': 'email,publish_actions',
    })
    return HttpResponseRedirect(fb_login_uri)
