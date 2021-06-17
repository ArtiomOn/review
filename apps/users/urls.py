from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.views import RegisterUserView, GetListUsers

urlpatterns = [
    path('user/list/', GetListUsers.as_view(), name='user-list'),
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
