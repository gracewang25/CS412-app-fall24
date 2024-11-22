from django.db import models

from django.db import models
from django.utils import timezone
import pytz
from django.contrib.auth.models import User


class Org(models.Model):
    """Org class for each unique organization."""

    # Data attributes
    name = models.TextField(blank=False)
    email = models.TextField(blank=False)
    location = models.TextField(blank=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    description = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)


    # FK to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='org')

    def __str__(self):
        return self.name

    def get_status_messages(self):
        # Convert timestamps to EST (Eastern Standard Time)
        est_tz = pytz.timezone('America/New_York')
        status_messages = self.status_messages.order_by('-timestamp')
        for status in status_messages:
            status.timestamp = status.timestamp.astimezone(est_tz)
        return status_messages

    def get_friends(self):
        friends1 = Friend.objects.filter(org1=self).values_list('org2', flat=True)
        friends2 = Friend.objects.filter(org2=self).values_list('org1', flat=True)
        return Org.objects.filter(id__in=list(friends1) + list(friends2))

    def add_friend(self, other):
        """Adds a friend if not already friends and not self-friending."""
        if self == other:
            return  # Prevent self-friending
        if not Friend.objects.filter(
            models.Q(org1=self, org2=other) | models.Q(org1=other, org2=self)
        ).exists():
            Friend.objects.create(org1=self, org2=other, timestamp=timezone.now())

    def get_friend_suggestions(self):
        """Returns a list of orgs not friends with self and excludes self."""
        current_friends = self.get_friends().values_list('id', flat=True)
        return Org.objects.exclude(id__in=current_friends).exclude(id=self.id)
    
class StatusMessage(models.Model):
    """Models the data attributes of Facebook status message."""
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.org.name}: {self.message[:30]}"

    def get_images(self):
        return Image.objects.filter(status_message=self)


class Image(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='status_images/')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for status {self.status_message.id} uploaded on {self.timestamp}"


class Friend(models.Model):
    org1 = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='org1')
    org2 = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='org2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.org1.name} & {self.org2.name}"


class InventoryItem(models.Model):
    ITEM_TYPES = [
        ('Costume', 'Costume'),
        ('Prop', 'Prop'),
        ('Other', 'Other'),
    ]

    org = models.ForeignKey(Org, related_name='inventory_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    # Size quantities
    size_xs = models.PositiveIntegerField(default=0, verbose_name="Extra Small Quantity")
    size_s = models.PositiveIntegerField(default=0, verbose_name="Small Quantity")
    size_m = models.PositiveIntegerField(default=0, verbose_name="Medium Quantity")
    size_l = models.PositiveIntegerField(default=0, verbose_name="Large Quantity")
    size_xl = models.PositiveIntegerField(default=0, verbose_name="Extra Large Quantity")    
    
    pricing_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Rental(models.Model):
    RENTAL_STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    seller = models.ForeignKey(
        Org, related_name='items_sold', on_delete=models.CASCADE
    )
    buyer = models.ForeignKey(
        Org, related_name='items_bought', on_delete=models.CASCADE, null=True, blank=True
    )
    item = models.ForeignKey('InventoryItem', related_name='rentals', on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()  # in days
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rental_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES)

    def __str__(self):
        return f"Rental ID: {self.id} - Item: {self.item.name} ( Seller: {self.seller} -> Buyer: {self.buyer})"