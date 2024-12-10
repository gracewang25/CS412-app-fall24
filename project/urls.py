# project/urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('inventory/', views.inventory_view, name='inventory'),
    path('browse/', views.browse_view, name='browse'),
    path('orders/', views.orders_view, name='orders'),
    path('org/<int:pk>/', views.org_view, name='org'),
    path('rent/<int:item_id>/', views.rent_item_view, name='rent_item'),
    path('post-item/', views.post_item_view, name='post_item'),

    path('checkout/<int:rental_id>/', checkout_view, name='checkout'),

    # Org Update
    path('org/<int:pk>/update/', OrgUpdateView.as_view(), name='org_update'),

    # Inventory Item Update and Delete
    path('inventory/<int:pk>/update/', InventoryItemUpdateView.as_view(), name='item_update'),
    path('inventory/<int:pk>/delete/', InventoryItemDeleteView.as_view(), name='item_delete'),

    # Status Message Update and Delete
    path('status/<int:pk>/update/', StatusMessageUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', StatusMessageDeleteView.as_view(), name='status_delete'),
]