# project/views.py

from django.shortcuts import render

# Create your views here.
from .models import *
from django.shortcuts import reverse, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


from django import template
from .forms import *

from django.conf import settings


# Profile page view
def org_view(request, pk):
    org = get_object_or_404(Org, pk=pk)
    status_messages = org.get_status_messages()
    return render(request, 'project/org.html', {
        'org': org,
        'status_messages': status_messages
    })

def inventory_view(request):
    inventory_items = InventoryItem.objects.filter(org=request.user.org)
    return render(request, 'project/inventory.html', {'inventory_items': inventory_items})

from django.shortcuts import render
from .models import Rental, InventoryItem


def browse_view(request):
    # Get the logged-in user's organization
    user_org = request.user.org

    # Fetch all items available for rent
    items_for_rent = InventoryItem.objects.filter(usage_type='rent')

    # Fetch user's friends
    friends = user_org.get_friends()

    # Split items into friends' items and others
    friends_items = [item for item in items_for_rent if item.org in friends]
    other_items = [item for item in items_for_rent if item.org not in friends]

    return render(request, 'project/browse.html', {
        'friends_items': friends_items,
        'other_items': other_items,
        'user_org': user_org,
    })

def orders_view(request):
    user_org = request.user.org
    in_progress_orders = Rental.objects.filter(buyer=user_org, rental_status='active')
    completed_orders = Rental.objects.filter(buyer=user_org, rental_status='completed')
    return render(request, 'project/orders.html', {
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
    })



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                # Redirect to the Org profile page
                org = user.org
                return redirect(reverse('org', args=[org.id]))
            except AttributeError:
                messages.error(request, "No organization is associated with this user.")
                return redirect('login')  # Stay on login page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'project/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

def register_view(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        org_form = OrgRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and org_form.is_valid():
            user = user_form.save()
            org = org_form.save(commit=False)
            org.user = user
            org.save()

            messages.success(request, "Registration successful.")
            return redirect('login')  # Redirect to login after successful registration
    else:
        user_form = UserRegistrationForm()
        org_form = OrgRegistrationForm()
    return render(request, 'project/register.html', {'user_form': user_form, 'org_form': org_form})


@login_required
def rent_item_view(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)

    # Prevent renting from one's own organization
    if item.org == request.user.org:
        messages.error(request, "You cannot rent items from your own organization.")
        return redirect('browse')

    # Prepare ranges for dropdowns in the template
    size_s_range = range(1, item.size_s + 1) if item.size_s else range(1)
    size_m_range = range(1, item.size_m + 1) if item.size_m else range(1)
    size_l_range = range(1, item.size_l + 1) if item.size_l else range(1)
    size_xl_range = range(1, item.size_xl + 1) if item.size_xl else range(1)
    prop_range = range(1, item.prop + 1) if item.prop else range(1)

    if request.method == "POST":
        # Get quantities for each size from the form
        quantity_prop = int(request.POST.get('prop', 0))
        quantity_s = int(request.POST.get('quantity_s', 0))
        quantity_m = int(request.POST.get('quantity_m', 0))
        quantity_l = int(request.POST.get('quantity_l', 0))
        quantity_xl = int(request.POST.get('quantity_xl', 0))

        # Calculate total cost
        total_quantity = quantity_s + quantity_m + quantity_l + quantity_xl + quantity_prop
        total_cost = total_quantity * item.pricing_per_unit

        # Create a rental entry
        rental = Rental.objects.create(
            seller=item.org,
            buyer=request.user.org,
            item=item,
            duration=1,  # Can add more functionality later
            total_cost=total_cost,
            rental_status='pending',
        )

        # Redirect to checkout
        return redirect('checkout', rental_id=rental.id)

    return render(request, 'project/rent_item.html', {
        'item': item,
        'size_s_range': size_s_range,
        'size_m_range': size_m_range,
        'size_l_range': size_l_range,
        'size_xl_range': size_xl_range,
        'prop_range': prop_range,
    })


@login_required
def post_item_view(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.org = request.user.org
            item.save()
            return redirect('inventory')  # Redirect to the inventory page
    else:
        form = InventoryItemForm()
    return render(request, 'project/post_item.html', {'form': form})

# Payment View

@login_required
def checkout_view(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    item = rental.item
    total_cost = rental.total_cost
    seller_venmo = rental.seller.venmo_username

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        if payment_method == "confirm_payment":
            rental.rental_status = 'active'
            rental.save()
            messages.success(request, "Payment confirmed! Your order is now active.")
            return redirect('orders')

    return render(request, 'project/checkout.html', {
        'rental': rental,
        'item': item,
        'total_cost': total_cost,
        'seller_venmo': seller_venmo,
    })


# Update Organization Profile
class OrgUpdateView(UpdateView):
    model = Org
    fields = ['name', 'profile_picture', 'venmo_username', 'description']  # Add relevant fields
    template_name = 'project/org_update.html'

    def get_success_url(self):
        return reverse_lazy('org', kwargs={'pk': self.object.id})

    def get_object(self, queryset=None):
        org = super().get_object(queryset)
        if org.user != self.request.user:
            raise PermissionDenied("You cannot edit this organization.")
        return org

# Update Inventory Item
class InventoryItemUpdateView(UpdateView):
    model = InventoryItem
    fields = ['name', 'description', 'item_type', 'pricing_per_unit', 'size_s', 'size_m', 'size_l', 'size_xl', 'prop', 'usage_type', 'image']
    template_name = 'project/item_update.html'

    def get_success_url(self):
        return reverse_lazy('inventory')

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        if item.org != self.request.user.org:
            raise PermissionDenied("You cannot edit items from other organizations.")
        return item

# Delete Inventory Item
class InventoryItemDeleteView(DeleteView):
    model = InventoryItem
    template_name = 'project/item_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('inventory')

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        if item.org != self.request.user.org:
            raise PermissionDenied("You cannot delete items from other organizations.")
        return item

# Update and Delete Status Messages
class StatusMessageUpdateView(UpdateView):
    model = StatusMessage
    fields = ['content']  # Include relevant fields
    template_name = 'project/status_update.html'

    def get_success_url(self):
        return reverse_lazy('org', kwargs={'pk': self.object.org.id})

class StatusMessageDeleteView(DeleteView):
    model = StatusMessage
    template_name = 'project/status_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('org', kwargs={'pk': self.object.org.id})