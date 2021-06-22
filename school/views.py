from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
import os, sys
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, Class
from .serializers import (
    CustomJWTSerializer, CustomUserSerializer, ChangePasswordSerializer,
    ClassSerializer
)

# Create your views here.

class JWTTokenObtainPairSerializer(TokenObtainPairView):
    """API to get JWT Token"""

    serializer_class = CustomJWTSerializer


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'list' \
                or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], name='change_password')
    def change_password(self, request):
        """
        API for changing password.
        old_password param:
        new_password param:
        """
        serializer_data = {
            'old_password': request.data.get('old_password'),
            'new_password': request.data.get('new_password')
        }

        serializer = ChangePasswordSerializer(
            request.user, data=serializer_data, partial=True
        )
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(e))
        return Response("Password changed", status=status.HTTP_200_OK)
        # return Response({}, data_status=status_, message=message)
