from datetime import date
from django.utils import timezone
from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Restaurant, Menu, Item
from .serializers import RestaurantSerializer, MenuSerializer, ItemSerializer
from employee.models import Vote, Employee


class RestaurantListCreate(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuListCreate(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']  # Получаем id ресторана из URL
        return Menu.objects.filter(restaurant_id=restaurant_id)


class ItemListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        menu_id = self.kwargs['menu_id']
        return Item.objects.filter(menu__restaurant_id=restaurant_id, menu__id=menu_id)


class CurrentDayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        today_votes = Vote.objects.filter(timestamp__date=date.today())
        top_menu = today_votes.values('menu').annotate(
            vote_count=Count('menu')).order_by('-vote_count').first()

        if top_menu:
            return Menu.objects.filter(id=top_menu['menu'], date=date.today())
        else:
            return Menu.objects.none()


class VotingResultsView(APIView):
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

            # Отримуємо ім'я та прізвище для кожного працівника
            employees_voted_names = []
            for employee_id in employees_voted_ids:
                employee = Employee.objects.get(id=employee_id)
                employee_name = f"{employee.user.first_name} {employee.user.last_name}"
                employees_voted_names.append(employee_name)

            menu_votes.append({'menu_id': menu_id, 'vote_count': vote_count, 'employees_voted': employees_voted_names})

        return Response(menu_votes)
