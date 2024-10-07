from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Profile class for each unique user.'''

    # data attributes:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)

    published = models.DateTimeField(auto_now=True)
    profile_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile.'''
        return f"{self.first_name} {self.last_name}"
    