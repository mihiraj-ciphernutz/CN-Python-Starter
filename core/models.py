import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email, password, and other fields.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hash password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with email, password, and other fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
    

class CustomUser(BaseModel, AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    is_owner = models.BooleanField(default=True)
    organizations = models.ManyToManyField('Organization', related_name='users', blank=True, through='UserOrganizationRole')
    roles = models.ManyToManyField('Role', related_name='users', blank=True, through='UserOrganizationRole')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Organization(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_organizations")


class Role(BaseModel):
    name = models.CharField(max_length=50, unique=True)


class UserOrganizationRole(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'core_user_organization_role'
        unique_together = ('customuser', 'organization', 'role')