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
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    description = models.TextField(blank=True)
    venmo_username = models.TextField(blank=True)  # New field

    published = models.DateTimeField(auto_now=True)


    # FK to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='org')

    def __str__(self):
        return self.name


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
    prop = models.PositiveIntegerField(default=0, verbose_name="Prop or Other Quantity")

    size_xs = models.PositiveIntegerField(default=0, verbose_name="Extra Small Quantity")
    size_s = models.PositiveIntegerField(default=0, verbose_name="Small Quantity")
    size_m = models.PositiveIntegerField(default=0, verbose_name="Medium Quantity")
    size_l = models.PositiveIntegerField(default=0, verbose_name="Large Quantity")
    size_xl = models.PositiveIntegerField(default=0, verbose_name="Extra Large Quantity")
    pricing_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    usage_type = models.CharField(
        max_length=10,
        choices=[('rent', 'For Rent'), ('storage', 'For Storage')],
        default='storage',
    )
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)  # New field

    @property
    def total_units(self):
        """Calculate the total number of units."""
        return self.prop + self.size_xs + self.size_s + self.size_m + self.size_l + self.size_xl

    def __str__(self):
        return self.name

from django.db.models.signals import pre_save
from django.dispatch import receiver

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
    rental_date = models.DateField()  # User-specified start date
    return_date = models.DateField(null=True, blank=True)  # User-specified end date
    duration = models.PositiveIntegerField(null=True, blank=True)  # Automatically calculated
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES)

    def is_overdue(self):
        """Check if the rental is overdue."""
        if self.return_date and self.rental_status == 'active':
            return timezone.now().date() > self.return_date
        return False

    def mark_as_overdue(self):
        """Mark the rental as overdue."""
        if self.is_overdue():
            self.rental_status = 'overdue'
            self.save()

    def is_available(self):
        """Check if the rental item should be available for browsing."""
        if self.rental_status == 'completed':
            return True  # Completed rentals make items available
        if self.return_date:
            return timezone.now().date() > self.return_date + timezone.timedelta(days=5)
        return False

    def __str__(self):
        return f"Rental ID: {self.id} - Item: {self.item.name} (Seller: {self.seller} -> Buyer: {self.buyer})"


@receiver(pre_save, sender=Rental)
def calculate_duration(sender, instance, **kwargs):
    """Automatically calculate the duration based on rental and return dates."""
    if instance.rental_date and instance.return_date:
        instance.duration = (instance.return_date - instance.rental_date).days