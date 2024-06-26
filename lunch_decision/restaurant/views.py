from datetime import date
from django.utils import timezone
from django.db.models import Count
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Restaurant, Menu, Item
from .serializers import RestaurantSerializer, MenuSerializer, ItemSerializer
from employee.models import Vote, Employee


class VersionedAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        version = request.headers.get('X-App-Version', None)

        if version == '2':
            raise NotFound("Version 2 is not supported yet")

        return super().dispatch(request, *args, **kwargs)


class RestaurantListCreate(VersionedAPIView, generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantRetrieveUpdateDestroy(VersionedAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuListCreate(VersionedAPIView):
    def get(self, request, restaurant_id):
        menus = Menu.objects.filter(id=restaurant_id)

        serializer = MenuSerializer(menus, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, restaurant_id):
        menus_data = request.data
        menus_serializer = MenuSerializer(data=menus_data)

        if menus_serializer.is_valid():
            menus_serializer.save(restaurant_id=restaurant_id)
            return Response(menus_serializer.data, status=status.HTTP_201_CREATED)
        return Response(menus_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuRetrieveUpdateDestroy(VersionedAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ItemListCreate(VersionedAPIView):
    def get(self, request, menu_id):
        items = Item.objects.filter(menu_id=menu_id)

        serializer = ItemSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, menu_id):
        # Remove all old items for this menu
        Item.objects.filter(menu_id=menu_id).delete()

        items_data = request.data
        items_serializer = ItemSerializer(data=items_data, many=True)

        if items_serializer.is_valid():
            items_serializer.save(menu_id=menu_id)
            return Response(items_serializer.data, status=status.HTTP_201_CREATED)
        return Response(items_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemRetrieveUpdateDestroy(VersionedAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CurrentDayMenuView(VersionedAPIView, generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        today_votes = Vote.objects.filter(timestamp__date=date.today())
        top_menu = today_votes.values('menu').annotate(
            vote_count=Count('menu')).order_by('-vote_count').first()

        if top_menu:
            return Menu.objects.filter(id=top_menu['menu'], date=date.today())
        else:
            return Menu.objects.none()


class VotingResultsView(VersionedAPIView, APIView):
    def get(self, request):
        today = timezone.now().date()
        results = Vote.objects.filter(timestamp__date=today).values('menu_id').annotate(
            vote_count=Count('employee')).order_by('-vote_count')

        menu_votes = []

        for result in results:
            menu_id = result['menu_id']
            vote_count = result['vote_count']
            employees_voted_ids = list(
                Vote.objects.filter(menu_id=menu_id, timestamp__date=today).values_list('employee', flat=True))

            employees_voted_names = []
            for employee_id in employees_voted_ids:
                employee = Employee.objects.get(id=employee_id)
                employee_name = f"{employee.user.first_name} {employee.user.last_name}"
                employees_voted_names.append(employee_name)

            menu_votes.append({'menu_id': menu_id, 'vote_count': vote_count, 'employees_voted': employees_voted_names})

        return Response(menu_votes)
