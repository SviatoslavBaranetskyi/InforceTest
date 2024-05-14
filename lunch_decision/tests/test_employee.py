import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from rest_framework import status
from datetime import datetime
from employee.models import Employee, Vote
from restaurant.models import Menu
from rest_framework.test import APIClient





@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "skydead",
        "email": "skydead@gmail.com",
        "password": "password",
        "first_name": "John",
        "last_name": "Doe",
        "employee_id": "EMP183",
        "department": "recruitment"
    }


@pytest.mark.django_db
def test_signup_view(client, user_data):
    url = reverse('register')
    response = client.post(url, user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_signin_view(client, user_data):
    user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
    url = reverse('login')
    response = client.post(url, user_data, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_profile_view(client, user_data):
    user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
    client.force_authenticate(user=user)

    employee = mixer.blend(Employee, user=user, employee_id=user_data['employee_id'], department=user_data['department'],)

    url = reverse('profile', kwargs={'user__username': user.username})

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['last_name'] == employee.user.last_name
    assert response.data['employee_id'] == employee.employee_id
    assert response.data['department'] == employee.department

    new_department = "Management"
    updated_data = {
        "department": new_department,
    }
    response = client.patch(url, updated_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['department'] == new_department

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_create_vote(client, user_data):
    user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
    client.force_authenticate(user=user)

    employee = mixer.blend(Employee, user=user, employee_id=user_data['employee_id'], department=user_data['department'])

    menu = mixer.blend(Menu)

    url = reverse('vote-create')

    response = client.post(url, {"menu": menu.id, "employee": employee.id}, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    assert Vote.objects.filter(employee=employee, menu=menu).exists()

