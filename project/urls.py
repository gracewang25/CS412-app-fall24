# project/urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # General nav links
    path('inventory/', views.inventory_view, name='inventory'),
    path('browse/', BrowseView.as_view(), name='browse'),
    path('orders/', views.orders_view, name='orders'),
    path('org/<int:pk>/', OrgProfileView.as_view(), name='org'),
    path('post-item/', views.post_item_view, name='post_item'),
    path('search/', SearchView.as_view(), name='search'),

     # Inventory URLs
    path('inventory/create/', CreateInventoryItemView.as_view(), name='create_inventory_item'),
    path('inventory/<int:pk>/update/', UpdateInventoryItemView.as_view(), name='update_inventory_item'),
    path('inventory/<int:pk>/delete/', DeleteInventoryItemView.as_view(), name='delete_inventory_item'),
    path('org/<int:org_id>/remove_friend/', remove_friend_view, name='remove_friend'),

    # Organization URLs
    path('org/<int:org_id>/add_friend/', add_friend_view, name='add_friend'),    path('rent/<int:item_id>/', views.rent_item_view, name='rent_item'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/delete/', DeleteProfileView.as_view(), name='delete_profile'),

    # Completing Orders
    path('rental/<int:rental_id>/complete/', complete_rental_view, name='complete_rental'),
    path('checkout/<int:rental_id>/', checkout_view, name='checkout'),

]