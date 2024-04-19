from datetime import datetime

from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MenuItemSerializer, UserSerializer, AddCartItemSerializer, CartSerializer, OrderSerializer, \
    OrderItemSerializer, PatchOrderSerializer, UpdateOrderSerializer
from rest_framework import generics, permissions, status
from LittleLemonAPI.models import MenuItem, Order, OrderItem
from .models import Cart


class Manager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['category__title']
    ordering_fields = ['price', 'inventory']

    def get_permissions(self):
        permission_classes = [Manager]
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = [Manager]
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


def extract_role_name(path):
    parts = path.split('/')
    if 'manager' in parts:
        return 'Manager'
    elif 'delivery-crew' in parts:
        return 'Delivery crew'


class ManagerListAddView(generics.ListCreateAPIView):
    permission_classes = [Manager]
    serializer_class = UserSerializer

    def get_queryset(self):
        role_name = extract_role_name(self.request.path)
        return User.objects.filter(groups__name=role_name)

    def post(self, request, *args, **kwargs):
        role_name = extract_role_name(self.request.path)
        username = request.data.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                manager_group = Group.objects.get(name=role_name)
                # Check if the user to be added is already a member of the "Manager" group
                if user.groups.filter(name=role_name).exists():
                    return Response({"message": f"{user.username} already {role_name}"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    manager_group.user_set.add(user)
                    return Response({"message": f"{user.username} added to {role_name} group."},
                                    status=status.HTTP_201_CREATED)
            else:
                return Response({"message": f"User with username {username} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Username not provided."},
                            status=status.HTTP_400_BAD_REQUEST)


class DeleteFromGroupView(generics.DestroyAPIView):
    permission_classes = [Manager]
    serializer_class = UserSerializer

    def get_queryset(self):
        role_name = extract_role_name(self.request.path)
        return User.objects.filter(groups__name=role_name)

    def delete(self, request, *args, **kwargs):
        username = request.data.get('username')
        role_name = extract_role_name(self.request.path)
        if username:
            try:
                user = User.objects.get(username=username)
                manager_group = Group.objects.get(name=role_name)
                manager_group.user_set.remove(user)
                return Response({"message": f"User {username} removed from {role_name} group."},
                                status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": f"User {username} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Username not provided."},
                            status=status.HTTP_400_BAD_REQUEST)


# class CartView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         cart_items = Cart.objects.filter(user=user)
#         if cart_items:
#             serializer = CartSerializer(many=True)
#             return Response(serializer.data)
#         else:
#             return Response(data={"error": "No cart"})
#
#     def post(self, request):
#         serializer = AddCartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # Сохраняем пользователя из запроса
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         user = request.user
#         cart_items = Cart.objects.filter(user=user)
#         if cart_items.exists():
#             cart_items.delete()
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "No items found in the cart."}, status=status.HTTP_404_NOT_FOUND)

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")


class OrdersView(APIView):

    def get(self, request):
        if request.user.groups.filter(name="Manager").exists():
            orders = Order.objects.all()
        elif request.user.groups.filter(name="Delivery crew").exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        elif request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "No items found in the cart."}, status=status.HTTP_400_BAD_REQUEST)

        order_data = {
            'user': request.user.id,
            'status': False,
            'total': sum(item.price for item in cart_items),
            'date': datetime.now().strftime("%Y-%m-%d"),
        }
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            cart_items.delete()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderIdView(APIView):

    def get(self, request, pk):
        """Change in models OrderItem field order_id on Order model instead a User Model cause it work very strange"""
        try:
            if Order.objects.filter(pk=pk):
                order_items = OrderItem.objects.filter(order_id=request.user)
                if order_items.exists():
                    serializer = OrderItemSerializer(order_items, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if request.user.groups.filter(name="Manager").exists():
                serializer = UpdateOrderSerializer(order, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "You do not have permission to update this order."},
                                status=status.HTTP_403_FORBIDDEN)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if order and request.user.groups.filter(name="Delivery crew").exists():
                serializer = PatchOrderSerializer(order, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            if request.user.groups.filter(name="Manager").exists():
                order = Order.objects.filter(pk=pk)
                if order.exists():
                    order.delete()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
