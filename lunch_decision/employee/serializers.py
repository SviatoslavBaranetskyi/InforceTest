from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, Vote


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    employee_id = serializers.CharField(max_length=255)
    department = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'employee_id', 'department']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        employee_id = validated_data.get('employee_id')
        department = validated_data.get('department')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Создаем запись Employee и связываем ее с пользователем
        employee = Employee.objects.create(user=user, employee_id=employee_id, department=department)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email', 'employee_id', 'department']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
