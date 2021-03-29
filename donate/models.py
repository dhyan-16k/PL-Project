from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
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

class User(AbstractUser):
    is_hospital = models.BooleanField(default = False)
    street = models.CharField (max_length=64)
    city = models.CharField (max_length=64)
    state = models.CharField (max_length=64)
    phone_no = PhoneNumberField(unique=True)
    blood_type = models.CharField(choices=unit_choices, max_length=64, blank=True)
    requests = models.ManyToManyField("User", blank=True, through="BloodRequest")

    def __str__(self):
        if self.is_hospital:
            return f'Hospital: {self.username}'
        else:
            return f'{self.username}'


class BloodRequest(models.Model):
    hospital = models.ForeignKey("User", on_delete=models.CASCADE, related_name="requester")
    donor = models.ForeignKey("User", on_delete=models.CASCADE, related_name="requested_donor")
    status_choice = [
        ("P", "Pending"),
        ("A", "Accepted"),
        ("D", "Denied")
    ]
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=status_choice, max_length=1, default="P")

    def __str__(self):
        return f"{self.id}: {self.hospital}->{self.donor}"


class DonationPlace(models.Model):
    name = models.CharField(max_length=64,unique=True)
    street = models.CharField (max_length=64)
    city = models.CharField (max_length=64)
    state = models.CharField (max_length=64)
    phone_no = PhoneNumberField(unique=True)
    donors = models.ManyToManyField(User, blank=True, related_name="donations")

    def __str__(self):
        return f"{self.id}: {self.name}"


class BloodBank(models.Model):
    dp_no = models.OneToOneField(DonationPlace, on_delete=models.CASCADE, related_name="bank")

    def __str__(self):
        return f'Blood Bank {self.id}'


class DonationCamp(models.Model):
    dp_no = models.OneToOneField(DonationPlace, on_delete=models.CASCADE, related_name="camp")
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f'Donation Camp {self.id}'

    def save(self, *args, **kwargs):
        if self.end_date >= self.start_date:
            super().save(*args, **kwargs)  # Call the "real" save() method.
        else:
            print("error")
            return


class BloodUnit(models.Model):

    blood_bank = models.ForeignKey("BloodBank", on_delete=models.CASCADE, related_name="blood_unit")
    blood_group = models.CharField(max_length=4, choices=unit_choices)
    no_of_units = models.IntegerField()

    def __str__(self):
        return f"{self.blood_bank} | {self.blood_group}"

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