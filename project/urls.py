from django.urls import path
from . import views

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

]