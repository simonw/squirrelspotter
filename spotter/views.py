from django.http import HttpResponse, HttpResponseRedirect
from common.shortcuts import render
from django.shortcuts import get_object_or_404
from spotter.models import Spotter, Spot
from django.conf import settings
from django.core.signing import Signer, BadSignature
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.db import transaction
from xml.etree import ElementTree as ET
import urllib, requests, cgi, datetime, json
import geohash

signer = Signer()

REDIRECT_URI = 'http://%s/login/done/'
SCORES_URL = 'https://graph.facebook.com/%s/scores' % settings.FB_APP_ID

@csrf_protect
def index(request):
    return render(request, 'index.html', {
        'user': user_from_request(request),
    })

def spot(request, id):
    spot = get_object_or_404(Spot, pk = id)
    user = user_from_request(request)
    is_new = datetime.datetime.utcnow() < spot.created + datetime.timedelta(seconds = 60)
    is_owner = spot.spotter == user
    return render(request, 'spot.html', {
        'spot': spot,
        'user': user,
        'is_new': is_new,
        'is_owner': is_owner,
    })

def debug(request):
    user = user_from_request(request)
    return HttpResponse(repr(user.__dict__ if user else None), content_type='text/plain')

@transaction.commit_manually
def create_spot(user, latitude, longitude, coords_json=''):
    spot = Spot.objects.create(
        spotter = user,
        latitude = latitude,
        longitude = longitude,
        coords_json = coords_json,
        geohash = geohash.encode(float(latitude), float(longitude)),
        location_name = reverse_geocode(latitude, longitude),
    )
    transaction.commit() # So facebook crawler can see it
    return spot

@csrf_protect
def spotted(request):
    user = user_from_request(request)
    assert user
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    coords_json = request.POST['coords_json']

    pk = create_spot(user, latitude, longitude, coords_json).pk

    requests.post('https://graph.facebook.com/me/squirrelspotter:spot', {
        'access_token': user.fb_access_token,
        'squirrel': 'http://www.squirrelspotter.com/spot/%s/' % pk,
    })
    # Update their score too
    requests.post('https://graph.facebook.com/me/scores', {
        'access_token': user.fb_access_token,
        'score': user.spots.count(),
    }, timeout=2)
    return HttpResponseRedirect('/spot/%s/' % pk)

def scores(request):
    user = user_from_request(request)
    if not user:
        return HttpResponseRedirect('/login/')
    scores = requests.get(SCORES_URL + '?' + urllib.urlencode({
        'access_token': user.fb_access_token
    })).json
    return render(request, 'scores.html', {
        'user': user,
        'scores': scores,
    })

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
        'redirect_uri': REDIRECT_URI % request.META['HTTP_HOST'],
        'scope': 'email,publish_actions',
    })
    return HttpResponseRedirect(fb_login_uri)

def done(request):
    code = request.GET['code']
    url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode({
        'client_id': settings.FB_APP_ID,
        'redirect_uri': REDIRECT_URI % request.META['HTTP_HOST'],
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
    except BadSignature:
        return None
    try:
        return Spotter.objects.get(pk = pk)
    except Spotter.DoesNotExist:
        return None

def reverse_geocode(latitude, longitude):
    url = "http://where.yahooapis.com/geocode?" + urllib.urlencode({
        "q": "%s,%s" % (latitude, longitude),
        "gflags": "R",
        "appid": "[yourappidhere]",
    })
    try:
        et = ET.fromstring(requests.get(url, timeout=3).text)
        d = dict([(e.tag, e.text) for e in et.find('Result')])
    except Exception, e:
        return None
    prefs = ('neighborhood', 'city', 'county', 'state', 'country')
    for pref in prefs:
        v = d.get(pref)
        if v:
            return v
    return None

@csrf_exempt
def twilio_sms(request):
    number = request.POST['From']
    body = request.POST['Body']
    try:
        user = Spotter.objects.get(phone_number = number)
        return twilio_sms_from_user(user, body)
    except Spotter.DoesNotExist:
        # Does the body match a code?
        if body:
            try:
                user = Spotter.objects.get(phone_number_token = body.lower())
            except Spotter.DoesNotExist:
                return HttpResponse('')
            user.phone_number = number
            user.save()
            return HttpResponse("""
                <?xml version="1.0" encoding="UTF-8"?>
                <Response>
                    <Sms from="+442033221149" to="%s">Hello %s! You can now report squirrels by texting a location to this number.</Sms>
                </Response>
            """ % (number, user.name))
        else:
            return HttpResponse('')

def twilio_sms_from_user(user, body):
    location = geocode(body)
    if location:
        spot = create_spot(user, location['latitude'], location['longitude'])
        return HttpResponse("""
            <?xml version="1.0" encoding="UTF-8"?>
            <Response>
                <Sms from="+442033221149" to="%s">Squirrel spotted! http://www.squirrelspotter.com/spot/%s/</Sms>
            </Response>
        """ % (user.phone_number, spot.pk))
    else:
        return HttpResponse("""
            <?xml version="1.0" encoding="UTF-8"?>
            <Response>
                <Sms from="+442033221149" to="%s">Sorry, that location didn't work - please try again</Sms>
            </Response>
        """ % user.phone_number)

def geocode(text):
    url = "http://where.yahooapis.com/geocode?" + urllib.urlencode({
        "q": text,
        "appid": "[yourappidhere]",
    })
    try:
        et = ET.fromstring(requests.get(url, timeout=3).text)
    except Exception, e:
        return None

    if et.find('Error').text != '0':
        return None

    latitude = et.find('Result/latitude').text
    longitude = et.find('Result/latitude').text
    return {
        'latitude': latitude,
        'longitude': longitude,
    }
