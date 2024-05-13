import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from rest_framework import status
from datetime import datetime
from employee.models import Employee, Vote
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


