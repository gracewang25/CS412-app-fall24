from django.shortcuts import render

# Create your views here.
from .models import *
from django.shortcuts import reverse, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import Org



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

def browse_view(request):
    # Get the current user's organization
    friends = request.user.org.get_friends()
    
    # Rentals from friends
    friends_rentals = Rental.objects.filter(org__in=friends)
    
    # Rentals from other organizations
    other_rentals = Rental.objects.exclude(org__in=friends).exclude(org=request.user.org)
    
    return render(request, 'project/browse.html', {
        'friends_rentals': friends_rentals,
        'other_rentals': other_rentals,
    })

def orders_view(request):
    in_progress_orders = Rental.objects.filter(org=request.user.org, rental_status='active')
    completed_orders = Rental.objects.filter(org=request.user.org, rental_status='completed')
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

def rent_item_view(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == "POST":
        duration = int(request.POST.get('duration', 1))  # Default to 1 day
        total_cost = duration * item.pricing_per_unit

        rental = Rental.objects.create(
            seller=item.org,
            buyer=request.user.org,
            item=item,
            duration=duration,
            total_cost=total_cost,
            rental_status='active',
        )

        return redirect('orders')  # Redirect to the orders page after renting

    return render(request, 'project/rent_item.html', {'item': item})


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