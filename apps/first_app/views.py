# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_reg.models import User
from .models import Trip
from datetime import date

# Create your views here.

def home(request):
    if not 'id' in request.session:
        messages.add_message(request, messages.ERROR, "Must be logged in!")
        return redirect("login:index")

    mytrip = Trip.objects.filter(others=User.objects.get(id=request.session["id"]))
    alltrips = Trip.objects.exclude(others=User.objects.get(id=request.session["id"]))

    context={
    "trips" : mytrip,
    "all_trips" : alltrips
    }

    return render(request, "first_app/index.html", context)

def destination(request, id):
    if not 'id' in request.session:
        messages.add_message(request, messages.ERROR, "Must be logged in!")
        return redirect("login:index")


    trip={
    "trip_item" : Trip.objects.get(id=id)
    }
    print "*****"
    print trip["trip_item"]

    return render(request, "first_app/destination.html", trip)

def jointrip(request, id):
    Trip.objects.JoinTrip(id, request.session["id"])
    return redirect("travels:home")

def add(request):
    if not 'id' in request.session:
        messages.add_message(request, messages.ERROR, "Must be logged in!")
        return redirect("login:index")
    return render(request, "first_app/add.html")

def post(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Wrong path dummy!")
        return redirect("travels:home")

    trip ={
    "creator" : User.objects.get(id=request.session["id"]),
    "place" : request.POST["place"],
    "plan" : request.POST["plan"],
    "start_date" : request.POST["start_date"],
    "end_date" : request.POST["end_date"]
    }

    response = Trip.objects.addTrip(trip)
    print "am i here?"
    print response

    if response['status'] == False:
        for error in response['errors']:
            print error
            messages.add_message(request, messages.ERROR, error)
        return redirect("travels:add")
    else:
        messages.add_message(request, messages.SUCCESS, "Cool, your trip has been made!" )
        return redirect("travels:home")
