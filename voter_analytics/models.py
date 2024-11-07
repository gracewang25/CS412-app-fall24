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

    Voter.objects.all().delete()


    with open('voter_analytics/newton_voters.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with transaction.atomic():
            for row in reader:
                Voter.objects.create(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'],
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=row['Date of Birth'],
                    date_of_registration=row['Date of Registration'],
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'] == 'TRUE',
                    v21town=row['v21town'] == 'TRUE',
                    v21primary=row['v21primary'] == 'TRUE',
                    v22general=row['v22general'] == 'True',
                    v23town=row['v23town'] == 'TRUE',
                    voter_score=int(row['voter_score'])
                )