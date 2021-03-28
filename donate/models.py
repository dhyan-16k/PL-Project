from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from datetime import date


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


class User (AbstractUser):
    is_hospital = models.BooleanField(default = False)
    street = models.CharField (max_length=50)
    area = models.CharField (max_length=50)
    city = models.CharField (max_length=50)
    state = models.CharField (max_length=50)
    phone_no = PhoneNumberField(unique=True)
    first_name = models.CharField( max_length=50)       # added to overwrite blank=False
    last_name = models.CharField( max_length=50)

    blood_type = models.CharField(choices=unit_choices, max_length=50, blank=True)
    #donors = models.ManyToManyField("User", blank=True, through="BloodRequests")

    def __str__(self):
        if self.is_hospital:
            return f'Hospital: {self.username}'
        else:
            return f'{self.username}'

class BloodRequests (models.Model):
    hospital = models.ForeignKey("User", on_delete=models.CASCADE, related_name="hospital")
    donor = models.ForeignKey("User", on_delete=models.CASCADE)
    status_choice = [
        ("P", "Pending"),
        ("A", "Accepted"),
        ("D", "Denied")
    ]
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=status_choice, max_length=1, default="P")


class DonationPlaces(models.Model):
    name = models.CharField(max_length=50,unique=True)
    street = models.CharField (max_length=50)
    city = models.CharField (max_length=50)
    state = models.CharField (max_length=50)
    phone_no = PhoneNumberField(unique=True)




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

    def save(self, *args, **kwargs):
        if self.end_date >= self.start_date:
            super().save(*args, **kwargs)  # Call the "real" save() method.
        else:
            print("error")
            return

    """class Meta ():
        #'start_date_check': 'check (start_date >= datetime.date.today() )',
        constraints = [
            models.CheckConstraint(check=Q( end_date >= start_date ), name="aap pehle chronology samajhiye")
        ]"""


"""
class Donor (AbstractUser):
    street = models.CharField (max_length=50)
    city = models.CharField (max_length=50)
    state = models.CharField (max_length=50)
    phone_no = PhoneNumberField(unique=True)

    blood_type = models.CharField(choices=unit_choices, max_length=50)

    donations = models.ManyToManyField(DonationPlaces)

    def __str__(self):
            return f'Blood Bank: {self.username}'


class Hospital (AbstractUser):
    dp_no = models.OneToOneField(DonationPlaces, on_delete=models.CASCADE)
    requests_made_to_donor = models.ManyToManyField(Donor, through='Requests', related_name="requested_donor")
    
    def __str__(self):
        return f'Blood Bank: {self.id}'


class Requests (models.Model):
    status_choice = [
        ("P", "Pending"),
        ("A", "Accepted"),
        ("D", "Denied")
    ]
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name="donor_no")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital_no")
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=status_choice, max_length=1, default="P")
"""


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