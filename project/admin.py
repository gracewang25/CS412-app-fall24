from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Org)
admin.site.register(Friend)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(InventoryItem)
admin.site.register(Rental)

