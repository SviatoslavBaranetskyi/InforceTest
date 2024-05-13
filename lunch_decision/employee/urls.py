from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignUpView, SignInView, ProfileView, VoteCreateView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('profile/<slug:user__username>/', ProfileView.as_view(), name='profile'),
    path('vote/', VoteCreateView.as_view(), name='vote-create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]