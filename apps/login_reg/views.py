# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "login_reg/index.html")

def register(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Sorry, gotta add something!")
        return redirect("/")

    person = {
    "first_name" : request.POST["first_name"],
    "last_name" : request.POST["last_name"],
    "email" : request.POST["email"],
    "pw" : request.POST["pw"],
    "confpw" : request.POST["confpw"],
    }

    response = User.objects.addUser(person)
    if response['status'] == False:
        for error in response['errors']:
            print error
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        messages.add_message(request, messages.SUCCESS, "You have registered!" )
        request.session["first_name"]=person["first_name"]
        request.session["id"]=response["person"].id
        return redirect("travels:home")


def login(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Sorry, gotta add something!")
        return redirect("/")

    person = {
    "email" : request.POST["email"],
    "pw" : request.POST["pw"],
    }

    response = User.objects.ValUser(person)
    print "WE ARE HERE!!"

    if response ["status"]:
        request.session["first_name"]=response["user"].first_name
        request.session["id"]=response["user"].id
        print request.session["id"]
        return redirect("travels:home")
    else:
        messages.add_message(request, messages.ERROR, "You must have valid credentials")
        return redirect("/")

def logout(request):
    request.session.flush()
    messages.add_message(request, messages.SUCCESS, "You have logged out!" )
    return redirect("/")
