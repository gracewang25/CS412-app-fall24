from django.shortcuts import render
import random
from datetime import datetime, timedelta

# Global Variables for Cat Café Menu Items
MENU_ITEMS = [
    {'name': 'Cat-puccino', 'price': 4.50, 'image': "https://cs-people.bu.edu/grace25/cat_images/image1.png"},
    {'name': 'Calico frappe', 'price': 5.00, 'image': "https://cs-people.bu.edu/grace25/cat_images/image2.png"},
    {'name': 'Kit-Tea Fog', 'price': 3.50, 'image': "https://cs-people.bu.edu/grace25/cat_images/image3.png"},
    {'name': 'Purrtado', 'price': 6.00, 'image': "https://cs-people.bu.edu/grace25/cat_images/image4.png"},
    {'name': 'Meowhito', 'price': 7.50, 'image': "https://cs-people.bu.edu/grace25/cat_images/image5.png"},
    {'name': 'Tuna Sandwich', 'price': 8.00, 'image': "https://cs-people.bu.edu/grace25/cat_images/image6.png"},
    {'name': 'Tira-meow-su', 'price': 6.50, 'image': "https://cs-people.bu.edu/grace25/cat_images/image7.png"},


]

DAILY_SPECIALS = [
    {'name': 'Biscof Cheescake', 'price': 9.00, 'image': "https://cs-people.bu.edu/grace25/cat_images/image8.png"},
    {'name': 'Pawcake Stack', 'price': 6.50, 'image': "https://cs-people.bu.edu/grace25/cat_images/image9.png"},
    {'name': 'Catnip Salad', 'price': 9.00, 'image': "https://cs-people.bu.edu/grace25/cat_images/image10.png"}
]

# Create your views here.

def main(request):
    # Select three random menu items to display on the main page
    featured_items = random.sample(MENU_ITEMS, 3)

    context = {
        'featured_items': featured_items
    }

    return render(request, 'restaurant/main.html', context)


def order(request):
    # Select a random daily special
    daily_special = random.choice(DAILY_SPECIALS)

    context = {
        'menu_items': MENU_ITEMS,
        'daily_special': daily_special['name'],
        'daily_special_price': daily_special['price'],
        'daily_special_image': daily_special['image']
    }

    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    if request.method == 'POST':
        selected_items_raw = request.POST.getlist('items')
        selected_items = []
        total_price = 0

        # Extract item names and prices from the submitted checkboxes
        for item_raw in selected_items_raw:
            name, price = item_raw.split('|')
            selected_items.append({'name': name, 'price': float(price)})
            total_price += float(price)

        customer_name = request.POST['name']
        customer_phone = request.POST['phone']
        customer_email = request.POST['email']
        special_instructions = request.POST.get('instructions', '')

        # Generate a random ready time
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        context = {
            'selected_items': selected_items,
            'total_price': total_price,
            'customer_name': customer_name,
            'ready_time': ready_time.strftime("%H:%M"),
            'special_instructions': special_instructions
        }

        return render(request, 'restaurant/confirmation.html', context)

    return render(request, 'restaurant/order.html')