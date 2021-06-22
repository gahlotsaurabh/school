from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class BaseContent(models.Model):
    """
        Captures BaseContent as created On and modified On and active field.
        common field accessed for the following classes.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.id


GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
]

ROLE_CHOICES = [
    ("SUPERADMIN", "SUPERADMIN"),
    ("ADMIN", "ADMIN"),
    ("STUDENT", "STUDENT")
]

class Class(BaseContent):
    name = models.CharField(_('name'), max_length=30, blank=True)

    def __str__(self):
        return self.name + str(self.id)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    # basic info
    profile_image = models.ImageField(
        _('profile image'), upload_to='profile_image', null=True, blank=True
    )
    student_class = models.ForeignKey(Class, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone_number = models.CharField(
        _('phone number'), max_length=15, blank=True
    )
    gender = models.CharField(
        _('gender'), choices=GENDER_CHOICES, blank=True, null=True,
        max_length=250
    )
    role = models.CharField(
        _('ROLE'), choices=ROLE_CHOICES, default="STUDENT", max_length=250
    )
    # inbuilt permission
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'), default=False, help_text=_(
            'Designates whether this student should be treated as active.'
            )
    )
    dob = models.DateField(_('date of birth'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
