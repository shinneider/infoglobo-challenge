from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_account(self, email, password, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=email, username=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        return self.create_account(email=email, password=password, is_staff=True,
                                   is_superuser=True, **kwargs)


class Account(AbstractUser):

    GENDER_CHOICES = [
        ("male", _("male")),
        ("female", _("female"))
    ]

    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=15, null=True, blank=True,
                              choices=GENDER_CHOICES, verbose_name=_("gender"))
    birthdate = models.DateField(null=True, blank=True, verbose_name=_("birthdate"))

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "account"

    def __str__(self):  # pragma: no cover
        return self.email

    def generate_account_username(self):
        name_splited = self.get_full_name().split(" ")

        if len(name_splited) > 1:
            username_base = '%s.%s' % (name_splited[0], name_splited[-1])
        else:
            username_base = self.first_name

        username = username_base
        username_rept = 1
        while(Account.objects.filter(username=username).exists()):
            username_rept += 1
            username = '%s.%s' % (username_base, username_rept)

        return username.lower()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.generate_account_username()

        super().save(*args, **kwargs)
