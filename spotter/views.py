from django.http import HttpResponse, HttpResponseRedirect
from common.shortcuts import render
from spotter.models import Spotter
from django.conf import settings
from django.core.signing import Signer
import urllib, requests, cgi, datetime, json

signer = Signer()

REDIRECT_URI = 'http://thawing-earth-2731.herokuapp.com/login/done/'

def index(request):
    return render(request, 'index.html', {
        'user': user_from_request(request),
    })

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
    r = requests.get(url)
    d = dict(cgi.parse_qsl(r.text))
    access_token = d['access_token']
    expires = int(d['expires'])
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds = expires)

    # Look up their details
    fb_json = requests.get('https://graph.facebook.com/me?access_token=%s' % access_token).text
    name = json.loads(fb_json)['name']
    fb_id = json.loads(fb_json)['id']

    spotter, created = Spotter.objects.get_or_create(fb_id = fb_id, defaults = {
        'name': name,
        'first_login': datetime.datetime.utcnow(),
    })
    spotter.fb_json = fb_json
    spotter.fb_access_token = access_token
    spotter.fb_access_token_expires = expires_at
    spotter.last_login = datetime.datetime.utcnow()
    spotter.save()

    response = HttpResponseRedirect('/')
    response.set_cookie('u', signer.sign(spotter.pk))
    return response

def user_from_request(request):
    cookie = request.COOKIES.get('u', '')
    try:
        pk = signer.unsign(cookie)
    except ValueError:
        return None
    try:
        return Spotter.objects.get(pk = pk)
    except Spotter.DoesNotExist:
        return None
