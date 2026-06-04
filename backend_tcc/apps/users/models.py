from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrador"),
        ("professor", "Professor"),
    )

    username = None
    email = None

    institutional_email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="professor")
    # Default False para nao afetar usuarios existentes (admin/superuser).
    # Ao criar um professor via UserCreateSerializer, o campo e forcado para True
    # para obrigar a troca de senha no primeiro login.
    must_change_password = models.BooleanField(default=False)

    USERNAME_FIELD = "institutional_email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_professor(self):
        return self.role == "professor"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.institutional_email
