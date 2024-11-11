# voter_analytics/models.py

from django.db import models
from django.db import transaction
import csv

# Create your models here.
class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
def reset():
       Voter.objects.all().delete()

def load_data():
    # Clear existing Voter records
    Voter.objects.all().delete()

    with open('voter_analytics/newton_voters.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with transaction.atomic():
            for row in reader:
                # Apply .strip() to each field to clean whitespace
                Voter.objects.create(
                    first_name=row['First Name'].strip(),
                    last_name=row['Last Name'].strip(),
                    street_number=row['Residential Address - Street Number'].strip(),
                    street_name=row['Residential Address - Street Name'].strip(),
                    apartment_number=row['Residential Address - Apartment Number'].strip() if row['Residential Address - Apartment Number'] else None,
                    zip_code=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=row['Date of Birth'].strip(),
                    date_of_registration=row['Date of Registration'].strip(),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'].strip(),

                    # Convert each election participation field to a boolean
                    v20state=row['v20state'].strip().lower() in ['true', '1', 'yes'],
                    v21town=row['v21town'].strip().lower() in ['true', '1', 'yes'],
                    v21primary=row['v21primary'].strip().lower() in ['true', '1', 'yes'],
                    v22general=row['v22general'].strip().lower() in ['true', '1', 'yes'],
                    v23town=row['v23town'].strip().lower() in ['true', '1', 'yes'],

                    voter_score=int(row['voter_score'].strip())
                )