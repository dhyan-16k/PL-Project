from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from .models import *
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST["search_city"]
        if city == 'Select Your City':
            dp_city = DonationPlace.objects.all()
            hospitals = User.objects.filter(is_hospital=True)
        else:
            dp_city = DonationPlace.objects.filter(city=city)
            hospitals = User.objects.filter(is_hospital=True, city=city)
        return render(request, "donate/index.html",{
            "camps": DonationCamp.objects.filter(dp_no__in=dp_city),
            "banks": BloodBank.objects.filter(dp_no__in=dp_city),
            "hospitals": hospitals
        })
    else:
        return render(request, "donate/index.html",{
            "camps": DonationCamp.objects.all(),
            "banks": BloodBank.objects.all(),
            "hospitals": User.objects.filter(is_hospital=True)
        })


@login_required
def profile(request):
    if request.user.is_hospital == False:
        donations = request.user.donations.all()
    return render(request, "donate/profile.html", {
        "donations": donations
    })


@login_required
def requests(request):
    if request.user.is_hospital == True:
        reqs = BloodRequest.objects.filter(hospital=request.user)
    else:
        reqs = BloodRequest.objects.filter(donor=request.user)
    return render(request, "donate/requests.html", {
        "reqs": reqs
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "donate/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "donate/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    return render(request, "donate/register.html")

def registerOption(request, option):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phoneNo = "+91" + request.POST["phone_no"]
        street = request.POST["street"]
        city = request.POST["city"]
        state = request.POST["state"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            if option == "hospital":
                return render(request, "donte/register_hospital.html", {
                    "message": "Passwords must match."
                })
            elif option == "donor":
                return render(request, "donate/register_donor.html", {
                    "message": "Passwords must match."
                })

        if option == "donor":
            blood_type = request.POST["blood_type"]
            first_name = request.POST["firstname"]
            last_name = request.POST["lastname"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.street = street
            user.city = city
            user.state = state
            user.phone_no = phoneNo
            if option == "donor":
                user.first_name = first_name
                user.last_name = last_name
                user.blood_type = blood_type
                user.is_hospital = False
            elif option == "hospital":
                user.is_hospital = True
            user.save()
        except IntegrityError:
            if option == "hospital":
                return render(request, "donate/register_hospital.html", {
                    "message": "Username already taken."
                })
            elif option == "donor":
                return render(request, "donate/register_donor.html", {
                    "message": "Username already taken."
                })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        if option == "hospital":
            return render(request, "donate/register_hospital.html")
        elif option == "donor":
            return render(request, "donate/register_donor.html")
        else:
            return HttpResponseRedirect(reverse(register))