# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User
from datetime import date
from time import strftime

today = strftime("%Y-%m-%d")

class TripManager(models.Manager):
    def addTrip(self, trip):
        response = {}
        errors = []
        if len(trip["place"].strip()) <1 or len(trip['plan'].strip()) <1 or len(trip['start_date'].strip()) <1 or len(trip['end_date'].strip()) <1:
            print "get out of here"
            errors.append("All fields must contain input!")
        if trip['start_date'] < str(date.today()):
            errors.append("You travel plans must be in the future")
        if trip['end_date'] < trip['start_date']:
            errors.append("Your end date cannot be before starting date")
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
            response['newtrip'] = Trip.objects.create(creator=trip["creator"], place=trip["place"], plan=trip["plan"], start_date=trip["start_date"], end_date=trip["end_date"])
            response['newtrip'].others.add(trip["creator"])
        return response

    def JoinTrip(self, id, user_id):
        trip=Trip.objects.get(id=id)
        trip.others.add(User.objects.get(id=user_id))
        return "You've Joined!"

class Trip(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    others = models.ManyToManyField(User, related_name="all_users")
    place = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()
