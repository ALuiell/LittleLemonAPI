from django.urls import path, include
from .views import *

urlpatterns = [
    path("menu-items", MenuItemsView.as_view(), name="menu-item"),
    path("menu-items/<int:pk>", SingleMenuItemView.as_view(), name="single-menu-item"),
    path('groups/manager/users', ManagerListAddView.as_view(), name="manager-user-list"),
    path('groups/manager/users/<int:pk>', DeleteFromGroupView.as_view(), name="delete-from-manager"),
    path('groups/delivery-crew/users', ManagerListAddView.as_view(), name="delivery-user-list"),
    path('groups/delivery-crew/users/<int:pk>', DeleteFromGroupView.as_view(), name="delete-from_delivery"),
    path('cart/menu-items', CartView.as_view(), name='cart-items'),
    path('orders', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderIdView.as_view(), name='orders-id'),
    path("", include("djoser.urls")),
]
