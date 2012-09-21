from django.http import HttpResponse, HttpResponseRedirect
from common.shortcuts import render
from django.conf import settings
import urllib, requests

REDIRECT_URI = 'http://thawing-earth-2731.herokuapp.com/login/done/'

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
    fb_login_uri = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode({
        'client_id': settings.FB_APP_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'email,publish_actions',
    })
    return HttpResponseRedirect(fb_login_uri)

def done(request):
    code = request.GET['code']
    url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode({
        'client_id': settings.FB_APP_ID,
        'redirect_uri': REDIRECT_URI,
        'client_secret': settings.FB_APP_SECRET,
        'code': code
    })
    return HttpResponse(str(requests.get(url)))
