from django.db import models
import datetime

class Spotter(models.Model):
    created = models.DateTimeField(default = datetime.datetime.utcnow)
    name = models.CharField(max_length = 128)
    fb_id = models.CharField(max_length = 128)
    fb_access_token = models.CharField(max_length = 128)
    phone_number = models.CharField(max_length = 50, blank=True, null=True)
    phone_number_token = models.CharField(max_length = 50, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Spot(models.Model):
    created = models.DateTimeField(default = datetime.datetime.utcnow)
    spotter = models.ForeignKey(Spotter)
    latitude = models.CharField(max_length = 32)
    longitude = models.CharField(max_length = 32)
    geohash = models.CharField(max_length = 16)
    location_name = models.CharField(max_length = 64, blank=True)
    #comment = 

    def __unicode__(self):
        return unicode(self.created)

#class SpotSubscription(models.Model):
#   spotter = 
#   geohash = 
