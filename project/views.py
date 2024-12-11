# project/views.py

from django.shortcuts import render

# Create your views here.
from .models import *

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils.timezone import now



from django import template
from .forms import *

from django.conf import settings

# Home page view
class HomePageView(TemplateView):
    template_name = 'project/home.html'
    
# Profile page view
class OrgProfileView(DetailView):
    model = Org
    template_name = 'project/org.html'
    context_object_name = 'org'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_org = self.request.user.org
        other_org = self.get_object()

        # Check if the current user can add this org as a friend
        context['can_add_friend'] = other_org not in user_org.get_friends() and other_org != user_org
        return context

def add_friend_view(request, org_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add friends.")
        return redirect('login')

    user_org = request.user.org
    other_org = get_object_or_404(Org, id=org_id)

    if other_org == user_org:
        messages.error(request, "You cannot add yourself as a friend.")
    elif other_org in user_org.get_friends():
        messages.error(request, f"{other_org.name} is already your friend.")
    else:
        user_org.add_friend(other_org)
        messages.success(request, f"You have successfully added {other_org.name} as a friend.")

    return redirect('org', pk=org_id)

@login_required
def remove_friend_view(request, org_id):
    """Handle removing a friend relationship."""
    if request.method == "POST":
        # Get the user's organization
        user_org = request.user.org
        # Get the other organization (friend)
        other_org = get_object_or_404(Org, id=org_id)

        # Look for the friendship in both directions
        friendship = Friend.objects.filter(
            models.Q(org1=user_org, org2=other_org) | models.Q(org1=other_org, org2=user_org)
        ).first()

        # Check if the friendship exists
        if friendship:
            friendship.delete()
            messages.success(request, f"You have removed {other_org.name} from your friends.")
        else:
            messages.error(request, f"{other_org.name} is not in your friends list.")

    # Redirect to the user's organization profile page
    return redirect(reverse('org', args=[user_org.id]))

# Inventory view
def inventory_view(request):
    inventory_items = InventoryItem.objects.filter(org=request.user.org)
    return render(request, 'project/inventory.html', {'inventory_items': inventory_items})


# Search View
class SearchView(ListView):
    model = InventoryItem
    template_name = 'project/search.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = InventoryItem.objects.all()

        # Filters
        org_id = self.request.GET.get('org_id')
        item_type = self.request.GET.get('item_type')
        size = self.request.GET.get('size')
        min_units = self.request.GET.get('min_units')
        max_units = self.request.GET.get('max_units')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        prop = self.request.GET.get('prop')

        # Apply filters
        if org_id:
            queryset = queryset.filter(org_id=org_id)

        if item_type:
            queryset = queryset.filter(item_type=item_type)

        if size and not prop:
            size_field = f"size_{size.lower()}"
            queryset = queryset.filter(**{f"{size_field}__gt": 0})

        if min_units:
            queryset = queryset.filter(
                Q(prop__gte=min_units) |
                Q(size_xs__gte=min_units) |
                Q(size_s__gte=min_units) |
                Q(size_m__gte=min_units) |
                Q(size_l__gte=min_units) |
                Q(size_xl__gte=min_units)
            )

        if max_units:
            queryset = queryset.filter(
                Q(prop__lte=max_units) |
                Q(size_xs__lte=max_units) |
                Q(size_s__lte=max_units) |
                Q(size_m__lte=max_units) |
                Q(size_l__lte=max_units) |
                Q(size_xl__lte=max_units)
            )

        if min_price:
            queryset = queryset.filter(pricing_per_unit__gte=min_price)

        if max_price:
            queryset = queryset.filter(pricing_per_unit__lte=max_price)

        if prop:
            queryset = queryset.filter(item_type='Prop')

        # Check if query returned results
        if not queryset.exists():
            messages.warning(self.request, "No items match the current filter criteria.")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orgs'] = Org.objects.all()  # Organizations for dropdown
        context['item_types'] = dict(InventoryItem.ITEM_TYPES)  # Item types for dropdown
        context['user_org'] = self.request.user.org  # Current user's organization
        return context

class BrowseView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'project/browse.html'
    context_object_name = 'items'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_org = self.request.user.org

        # Additional context for original browse grid
        base_items = InventoryItem.objects.filter(
            Q(rentals__rental_status='completed') |
            ~Q(rentals__rental_status='active'),
            usage_type='rent'
        ).distinct()

        friends = user_org.get_friends()
        context['friends_items'] = base_items.filter(org__in=friends)
        context['other_items'] = base_items.exclude(org__in=friends)

        # Context for filter form
        context['orgs'] = Org.objects.all()  # Organizations for dropdown
        context['item_types'] = dict(InventoryItem.ITEM_TYPES)  # Item types for dropdown
        context['user_org'] = user_org

        return context

@login_required
def orders_view(request):
    user_org = request.user.org
    
    # Orders where the user is the buyer
    in_progress_orders = Rental.objects.filter(buyer=user_org, rental_status='active')
    overdue_orders = Rental.objects.filter(buyer=user_org, rental_status='overdue')
    completed_orders = Rental.objects.filter(buyer=user_org, rental_status='completed')
    
    # Orders where the user is the seller
    selling_orders_in_progress = Rental.objects.filter(seller=user_org, rental_status='active')
    selling_orders_overdue = Rental.objects.filter(seller=user_org, rental_status='overdue')
    selling_orders_completed = Rental.objects.filter(seller=user_org, rental_status='completed')
    
    return render(request, 'project/orders.html', {
        'in_progress_orders': in_progress_orders,
        'overdue_orders': overdue_orders,
        'completed_orders': completed_orders,
        'selling_orders_in_progress': selling_orders_in_progress,
        'selling_orders_overdue': selling_orders_overdue,
        'selling_orders_completed': selling_orders_completed,
    })

@login_required
def complete_rental_view(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    
    if rental.rental_status == 'active':
        if rental.buyer == request.user.org or rental.seller == request.user.org:
            rental.rental_status = 'completed'
            rental.save()
            messages.success(request, "Rental marked as completed.")
        else:
            messages.error(request, "You do not have permission to complete this rental.")
    else:
        messages.error(request, "This rental cannot be completed.")

    return HttpResponseRedirect(reverse('orders'))

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


from datetime import datetime

@login_required
def rent_item_view(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)

    # Prevent renting from one's own organization
    if item.org == request.user.org:
        messages.error(request, "You cannot rent items from your own organization.")
        return redirect('browse')

    # Prepare ranges for dropdowns in the template
    size_s_range = range(0, item.size_s + 1) if item.size_s else range(1)
    size_m_range = range(0, item.size_m + 1) if item.size_m else range(1)
    size_l_range = range(0, item.size_l + 1) if item.size_l else range(1)
    size_xl_range = range(0, item.size_xl + 1) if item.size_xl else range(1)
    prop_range = range(0, item.prop + 1) if item.prop else range(1)

    if request.method == "POST":
        # Get rental start and end dates
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')

        # Convert dates to datetime objects
        try:
            rental_date = datetime.strptime(rental_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect(request.path)

        # Ensure return date is after rental date
        if return_date <= rental_date:
            messages.error(request, "Return date must be after the rental date.")
            return redirect(request.path)

        # Calculate duration
        duration = (return_date - rental_date).days

        # Get quantities for each size from the form
        quantity_prop = int(request.POST.get('prop', 0))
        quantity_s = int(request.POST.get('quantity_s', 0))
        quantity_m = int(request.POST.get('quantity_m', 0))
        quantity_l = int(request.POST.get('quantity_l', 0))
        quantity_xl = int(request.POST.get('quantity_xl', 0))

        # Calculate total cost
        total_quantity = quantity_s + quantity_m + quantity_l + quantity_xl + quantity_prop
        total_cost = total_quantity * item.pricing_per_unit * duration

        # Create a rental entry
        rental = Rental.objects.create(
            seller=item.org,
            buyer=request.user.org,
            item=item,
            rental_date=rental_date,
            return_date=return_date,
            duration=duration,
            total_cost=total_cost,
            rental_status='active',
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
    template_name = 'project/up/org_update.html'

    def get_success_url(self):
        return reverse_lazy('org', kwargs={'pk': self.object.id})

    def get_object(self, queryset=None):
        org = super().get_object(queryset)
        if org.user != self.request.user:
            raise PermissionDenied("You cannot edit this organization.")
        return org

# Inventory Item Views
class CreateInventoryItemView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'project/up/create_inventory_item.html'

    def form_valid(self, form):
        form.instance.org = self.request.user.org
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('inventory')


from django.shortcuts import redirect

class UpdateInventoryItemView(UpdateView):
    model = InventoryItem
    fields = [
        "name",
        "description",
        "item_type",
        "usage_type",
        "pricing_per_unit",
        "prop",
        "size_xs",
        "size_s",
        "size_m",
        "size_l",
        "size_xl",
        "image",
    ]
    template_name = "project/up/update_inventory_item.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        item_type = self.object.item_type

        if item_type == "Prop":
            # Only `prop` is needed; hide and make other size fields optional
            form.fields["size_xs"].widget = forms.HiddenInput()
            form.fields["size_xs"].required = False
            form.fields["size_s"].widget = forms.HiddenInput()
            form.fields["size_s"].required = False
            form.fields["size_m"].widget = forms.HiddenInput()
            form.fields["size_m"].required = False
            form.fields["size_l"].widget = forms.HiddenInput()
            form.fields["size_l"].required = False
            form.fields["size_xl"].widget = forms.HiddenInput()
            form.fields["size_xl"].required = False
        else:
            # Hide `prop` and make it optional
            form.fields["prop"].widget = forms.HiddenInput()
            form.fields["prop"].required = False

        return form

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        if item.org != self.request.user.org:
            raise PermissionDenied("You cannot edit items from other organizations.")
        return item

    def get_success_url(self):
        return reverse_lazy("inventory")
    
class DeleteInventoryItemView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'project/up/delete_inventory_item.html'

    def get_object(self):
        item = super().get_object()
        if item.org != self.request.user.org:
            raise PermissionDenied("You cannot delete items from other organizations.")
        return item

    def get_success_url(self):
        return reverse_lazy('inventory')




# Update Profile View
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Org
    form_class = OrgUpdateForm
    template_name = 'project/up/update_profile.html'

    def get_object(self):
        """Ensure users can only update their own organization profile."""
        profile = super().get_object()
        if profile.user != self.request.user:
            raise PermissionDenied("You can only update your own profile.")
        return profile

    def get_success_url(self):
        return reverse_lazy('org', kwargs={'pk': self.object.pk})


# Delete Profile View
class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = Org
    template_name = 'project/up/delete_profile.html'

    def get_object(self):
        """Ensure users can only delete their own organization profile."""
        profile = super().get_object()
        if profile.user != self.request.user:
            raise PermissionDenied("You can only delete your own profile.")
        return profile

    def get_success_url(self):
        """Log the user out after profile deletion and redirect to login."""
        from django.contrib.auth import logout
        logout(self.request)
        return reverse_lazy('login')