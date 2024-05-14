import pytest
from django.urls import reverse
from rest_framework import status
from mixer.backend.django import mixer
from datetime import date
from employee.models import Vote, Employee
from restaurant.models import Restaurant, Menu, Item


@pytest.mark.django_db
def test_current_day_menu_view(client):
    restaurant = mixer.blend(Restaurant)
    menu = mixer.blend(Menu, restaurant=restaurant, date=date.today())
    vote = mixer.blend(Vote, menu=menu)

    url = reverse('current-day-menu')
    response = client.get(url)
    print(response.data)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == menu.id


@pytest.mark.django_db
def test_voting_results_view(client):
    employee1 = mixer.blend(Employee)
    employee2 = mixer.blend(Employee)
    employee3 = mixer.blend(Employee)

    menu1 = mixer.blend(Menu)
    menu2 = mixer.blend(Menu)

    mixer.blend(Vote, menu=menu1, employee=employee1, timestamp=date.today())
    mixer.blend(Vote, menu=menu1, employee=employee2, timestamp=date.today())

    mixer.blend(Vote, menu=menu2, employee=employee3, timestamp=date.today())

    url = reverse('voting-results')

    response = client.get(url)

    print(response.data)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2

    assert response.data[0]['vote_count'] == 2
    assert response.data[1]['vote_count'] == 1


@pytest.mark.django_db
def test_voting_results_view_no_votes(client):
    url = reverse('voting-results')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
