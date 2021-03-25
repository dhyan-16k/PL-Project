from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
# Create your models here.

unit_choices = [
    ("AB-", "AB Negative"),
    ("AB+", "AB Positive"),
    ("A-", "A Negative"),
    ("A+", "A Positive"),
    ("B-", "B Negative"),
    ("B+", "B Positive"),
    ("O-", "O Negative"),
    ("O+", "O Positive")
]

"""
class User (AbstractUser):
    is_hospital = models.BooleanField(default = False)
    blood_group = models.CharField(choices=unit_choices, max_length=4, blank=True, null=True)
    donors = models.ManyToManyField("User")

    def __str__(self):
        if self.is_hospital:
            return f'Hospital: {self.username}'
        else:
            return f'{self.username}'
"""

class DonationPlaces(models.Model):
    name = models.CharField(max_length=50,unique=True)
    street = models.CharField (max_length=50)
    city = models.CharField (max_length=50)
    state = models.CharField (max_length=50)
    phone_no = models.PhoneNumberField(unique=True)




class BloodBank (models.Model):
    dp_no = models.OneToOneField(DonationPlaces, on_delete=models.CASCADE)
    def __str__(self):
        return f'Blood Bank: {self.id}'


class DonationCamp (models.Model):
    dp_no = models.OneToOneField(DonationPlaces, on_delete=models.CASCADE)

    start_date = models.DateField( auto_now_add=False)
    end_date = models.DateField( auto_now_add=False)

    def __str__(self):
        return f'Donation Camp: {self.id}'




class Donor (AbstractUser):
    street = models.CharField (max_length=50)
    city = models.CharField (max_length=50)
    state = models.CharField (max_length=50)
    phone_no = models.PhoneNumberField(unique=True)

    blood_type = models.CharField(choices=unit_choices, max_length=50)

    donations = models.ManyToManyField(DonationPlaces)

    def __str__(self):
            return f'Blood Bank: {self.username}'


class Hospital (AbstractUser):
    dp_no = models.OneToOneField(DonationPlaces, on_delete=models.CASCADE)
    requests = models.ManyToManyField(Donor, through=Requests)
    
    def __str__(self):
        return f'Blood Bank: {self.id}'


class Requests (models.Model):
    status_choice = [
        ("P", "Pending"),
        ("A", "Accepted"),
        ("D", "Denied")
    ]
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=status_choice, max_length=1, default="P")


class BloodUnits (models.Model):

    blood_bank = models.ForeignKey("BloodBank", on_delete=models.CASCADE, related_name="blood_unit")
    blood_group = models.CharField(max_length=4, choices=unit_choices)
    no_of_units = models.IntegerField()

    class Meta :
        unique_together = ("id", "blood_bank") 


"""
 
Donors :
Donor_id
Name
Email
Phone no
Address (street, area,city)
Blood_type
 
Donation places:
Name
Address (street, area,city)
Phone_no
email
 
Hospitals / recievers :
Hospital_id

Donation Camps:
Start date
End date
Timing


Blood banks (store house)


Blood units
(weak entity ?)
Blood group
No of units
 
"""