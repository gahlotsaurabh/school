from django.db.models import fields
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Class, CustomUser
from rest_framework.serializers import CharField, ValidationError, Serializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude:
            # Drop fields that are specified in the `exclude` argument.
            excluded = set(exclude)
            for field_name in excluded:
                try:
                    self.fields.pop(field_name)
                except KeyError:
                    pass


class ClassSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Class
        fields = ('__all__')

class CustomUserSerializer(DynamicFieldsModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id", "email", "full_name", "last_login", "gender", "dob",
            "profile_image", "first_name", "last_name", "phone_number",
            "student_class"
            )
        extra_kwargs = {
            'is_active': {'write_only': True},
            'is_staff': {'write_only': True},
            'password': {'write_only': True}
        }

    def get_full_name(self, obj):
        return ' '.join(filter(None, (obj.first_name, obj.last_name)))


class CustomJWTSerializer(TokenObtainPairSerializer):
    """Serializer for JWT."""

    def validate(self, attrs):
        """Override validation."""
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        if not self.user.is_active:
            raise ValidationError
        data['user'] = CustomUserSerializer(
            self.user, fields=('id', 'full_name', 'profile_image', 'email')
        ).data
        data['user']['is_admin'] = self.user.is_superuser
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class ChangePasswordSerializer(Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = CharField(required=True)
    new_password = CharField(required=True)

    def update(self, instance, validated_data):
        password_valid = instance.check_password(
            validated_data.get('old_password'))
        if not password_valid:
            error = {'error': "Wrong password"}
            raise ValidationError(error)

        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance
