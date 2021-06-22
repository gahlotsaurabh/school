from django.urls import path, include
from rest_framework import routers
from .views import (
    JWTTokenObtainPairSerializer
    )
from .views import CustomUserViewSet, ClassViewSet
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()

router.register(r'user', CustomUserViewSet)
router.register(r'class', ClassViewSet)

urlpatterns = [
    path(
        'v1/token/', JWTTokenObtainPairSerializer.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/', jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/', include(router.urls)),
]
