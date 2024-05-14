# Lunch Decision
This project is an internal service for a company to help its employees decide where to eat lunch.
## Idea
The project aims to streamline the lunch decision process for employees within the company. It features an internal service that facilitates the selection of lunch venues. Restaurants have the capability to upload their menus seamlessly through an API integration. The backend infrastructure is designed to efficiently manage requests originating from various versions of the application, dynamically adapting to the build number information provided in the request headers.
# Technological stack
- Django
- Django Rest Framework
- JWT
- PostgreSQL
- Docker
- PyTests
# Starting a project
- Run the Docker container:
```
docker compose up -d
```
# API Endpoints:
## Requests that do not require a token:
## Employees
- Register a user<br>
POST /api/auth/register/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"username": "username",<br>
&nbsp;&nbsp;&nbsp;"password": "password",<br>
&nbsp;&nbsp;&nbsp;"email": "username@gmail.com",<br>
&nbsp;&nbsp;&nbsp;"first_name": "Name",<br>
&nbsp;&nbsp;&nbsp;"last_name": "Surname",<br>
&nbsp;&nbsp;&nbsp;"employee_id": "EMP183",<br>
&nbsp;&nbsp;&nbsp;"department": "IT"<br>
}
- User authorization<br>
POST /api/auth/login/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"username": "username",<br>
&nbsp;&nbsp;&nbsp;"password": "password"<br>
}
- Update access token<br>
POST api/auth/token/refresh/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"refresh": "token_refresh"<br>
}<br>
## Restaurants
- Retrieve a list of all restaurants<br>
GET /api/restaurants/
- Retrieve a specific restaurant by its primary key<br>
GET /api/restaurants/&lt;int:pk&gt;/
- Update restaurant info<br>
PUT /api/restaurants/&lt;int:pk&gt;/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "Name",<br>
&nbsp;&nbsp;&nbsp;"address": "Street, City, Code",<br>
&nbsp;&nbsp;&nbsp;"phone_number": "+3801235489987",<br>
&nbsp;&nbsp;&nbsp;"description": "description"<br>
}
- Partial update restaurant info<br>
PATCH /api/restaurants/&lt;int:pk&gt;/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "Name",<br>
}
- Delete restaurant<br>
DELETE /api/restaurants/&lt;int:pk&gt;/<br>
- Retrieve a list of all menus<br>
GET /api/restaurants/&lt;int:pk&gt;/menus/
- Retrieve a specific menu by its primary key<br>
GET /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:pk&gt;/
- Update menu info<br>
PUT /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:pk&gt;/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"date": "2024-05-13",<br>
&nbsp;&nbsp;&nbsp;"description": "description",<br>
&nbsp;&nbsp;&nbsp;"restaurant": 1<br>
}
- Partial update menu info<br>
PATCH /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:pk&gt;/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"description": "description",<br>
}
- Delete menu<br>
DELETE /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:pk&gt;/
- Retrieve a list of all items<br>
GET /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:menu_id&gt;/items/
- Retrieve a specific item by its primary key<br>
GET /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:menu_id&gt;/items/&lt;int:pk&gt;/
- Update item info<br>
PUT /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:menu_id&gt;/items/&lt;int:pk&gt;/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "name",<br>
&nbsp;&nbsp;&nbsp;"price": "210.00",<br>
&nbsp;&nbsp;&nbsp;"description": "description",<br>
&nbsp;&nbsp;&nbsp;"menu": 1<br>
}
- Partial update item info<br>
PATCH /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:menu_id&gt;/items/&lt;int:pk&gt;/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"description": "description",<br>
}
- Delete item<br>
DELETE /api/restaurants/&lt;int:restaurant_id&gt;/menus/&lt;int:menu_id&gt;/items/&lt;int:pk&gt;/
- Retrieve current day menu<br>
GET /api/restaurants/current_day_menu/
- Retrieve menu voting results<br>
GET /api/restaurants/voting_results/
## Requests that require a token (Authorization: Bearer your-access-token):
- Retrieve a user profile<br>
GET /api/auth/profile/{username}/
- Update profile<br>
PUT /api/auth/profile/{username}/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"first_name": "Name",<br>
&nbsp;&nbsp;&nbsp;"last_name": "Surname",<br>
&nbsp;&nbsp;&nbsp;"employee_id": "EMP123",<br>
&nbsp;&nbsp;&nbsp;"department": "IT",<br>
&nbsp;&nbsp;&nbsp;"email": "username@gmail.com"<br>
}
- Partial update profile<br>
PATCH /api/auth/profile/{username}/<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"department": "IT",<br>
}
- Delete profile<br>
DELETE /api/auth/profile/{username}/
- Create a vote<br>
POST /api/v1/auth/vote/
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"menu": 1,<br>
&nbsp;&nbsp;&nbsp;"employee": 7<br>
}
# API Versioning:
At present, only version 1 is enabled and operational. All the endpoints and tests described below are designed for this version. However, all necessary preparations have been made to introduce new features with version 2.
# Future plans:
- Introducing the ability to rate restaurants and menus through reviews and ratings.
- Development of a recommendation system based on user preferences and voting results.
- The ability to upload multiple menus, each tailored to a specific audience. For example, vegetarian, gluten-free menus, etc.
## Developer
- Sviatoslav Baranetskyi<br>
  Email: svyatoslav.baranetskiy738@gmail.com
