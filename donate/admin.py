from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(DonationPlaces)
admin.site.register(DonationCamp)
admin.site.register(BloodBank)
admin.site.register(BloodUnits)
admin.site.register(Hospital)
admin.site.register(Donor)
admin.site.register(Requests)