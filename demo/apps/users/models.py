from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db.models import  QuerySet,Manager
from django.utils.translation import gettext_lazy  as _
from django.utils import timezone


# Create your models here.


user_choices=(
    ("1","customer"),
    ("2","supplier")
)

class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)

    def delete(self):
        """Mark the record as deleted instead of deleting it"""

        self.is_deleted = True
        self.save()
    def restore(self):
        self.is_deleted=False
        self.save()







class AppQuerySet(QuerySet):
    def delete(self):
        """ use to delete users """
        self.update(is_deleted=True)

    def restore_deleted(self):
        """ use to restore deleted users"""
        if self.is_deleted==False:
            raise ValueError('the object is not deleted')

        self.update(is_deleted=False)


class soft_delete_manager(models.Manager):
    def get_queryset(self):
        """returns a query set for all the no deleted user"""
        return AppQuerySet(self.model, using=self._db).exclude(is_deleted=True)

    def filter_deleted(self,**kwargs):
        """returns a query set with filter for deleted user"""
        return AppQuerySet(self.model, using=self.db).exclude(is_deleted=False).filter(**kwargs)
    def get_deleted(self,**kwargs):
        """
        returns specific deleted users
        """
        return AppQuerySet(self.model, using=self.db).exclude(is_deleted=False).get(**kwargs)





class UserManager(soft_delete_manager,BaseUserManager):
    def _create_user(self, email, username="", password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        now = timezone.now()
        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username="", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username="", password=None, **extra_fields):
        """
        Create and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class User(BaseModel,AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"), unique=True, blank=False, max_length=254, validators=[]
    )

    active = models.BooleanField(_("active"), default=False, help_text=_("Active user"))

    first_name = models.CharField(_("First Name"), max_length=254, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=254, blank=True)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    authorization=models.CharField(max_length=10,choices=user_choices,default=1)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
            "Unselect this instead of deleting accounts."
        ),
    )
    date_created = models.DateTimeField(_("date created"), default=timezone.now)
    objects= UserManager()
    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "users"
        ordering = ["-date_created", "email"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["first_name", "last_name"]),
        ]


class adress(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    zipcode=models.IntegerField()
    houseno=models.IntegerField()
    locality=models.CharField(max_length=500)
    city=models.CharField(max_length=255)
    state=models.CharField(max_length=255)

    def __str__(self):
        return str(self.zipcode)+"  "+str(self.houseno)+"  "+str(self.locality)+"  "+str(self.city)+"  "+str(self.state)
