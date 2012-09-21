from django.db import models
import datetime, hashlib, random

class Spotter(models.Model):
    created = models.DateTimeField(default = datetime.datetime.utcnow)
    name = models.CharField(max_length = 128)
    fb_id = models.CharField(max_length = 128)
    fb_json = models.TextField()
    fb_access_token = models.CharField(max_length = 128)
    fb_access_token_expires = models.DateTimeField(null = True, blank = True)
    phone_number = models.CharField(max_length = 50, blank=True, null=True)
    phone_number_token = models.CharField(
        max_length = 50, blank=True, null=True,
        default = lambda: hashlib.sha1(str(random.random())).hexdigest()[:8]
    )

    first_login = models.DateTimeField(null = True, blank = True)
    last_login = models.DateTimeField(null = True, blank = True)

    def __unicode__(self):
        return self.name

class Spot(models.Model):
    created = models.DateTimeField(default = datetime.datetime.utcnow)
    spotter = models.ForeignKey(Spotter, related_name = 'spots')
    latitude = models.CharField(max_length = 32)
    longitude = models.CharField(max_length = 32)
    geohash = models.CharField(max_length = 16)
    coords_json = models.TextField()
    location_name = models.CharField(max_length = 64, blank=True)
    #comment = 

    def __unicode__(self):
        return unicode(self.created)

#class SpotSubscription(models.Model):
#   spotter = 
#   geohash = 
