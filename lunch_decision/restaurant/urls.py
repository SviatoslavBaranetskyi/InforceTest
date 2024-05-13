from django.urls import path
from .views import *

urlpatterns = [
    path('', RestaurantListCreate.as_view(), name='restaurant-list'),
    path('<int:pk>/', RestaurantRetrieveUpdateDestroy.as_view(), name='restaurant-detail'),
    path('<int:pk>/menus/', MenuListCreate.as_view(), name='menu-list'),
    path('<int:restaurant_id>/menus/<int:pk>/', MenuRetrieveUpdateDestroy.as_view(), name='menu-detail'),
    path('<int:restaurant_id>/menus/<int:menu_id>/items/', ItemListCreate.as_view(), name='item-list'),
    path('<int:restaurant_id>/menus/<int:menu_id>/items/<int:pk>/', ItemRetrieveUpdateDestroy.as_view(), name='item-detail'),
    path('current_day_menu/', CurrentDayMenuView.as_view(), name='current-day-menu'),
    path('voting_results/', VotingResultsView.as_view(), name='voting-results'),
]
