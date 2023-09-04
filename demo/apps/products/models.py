from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy  as _
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

user_choices=(
    ("1","customer"),
    ("2","supplier")
)

del_status=(
    ("1","delieverd"),
    ("2","not delieverd")
)


class UserManager(BaseUserManager):
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


class User(AbstractBaseUser, PermissionsMixin):
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

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=1000, default='',blank=True)
    available_units=models.PositiveIntegerField(default=0)
    price_per_unit=models.PositiveIntegerField(null=True)
    supplier=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

    @staticmethod
    def get_products(key):

        return Product.objects.filter(id__in=key)


class cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @staticmethod
    def cart_product(id):
        return Product.get_products([i.product.id for i in cart.objects.filter(user=id)])
    @staticmethod
    def cart_objects(id):
        return cart.objects.filter(user=id)

class Product_image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image_link=models.URLField()


    
class order(models.Model):
    secret_key=models.CharField(max_length=20)
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    del_adress=models.ForeignKey(adress,on_delete=models.DO_NOTHING)
    final_price=models.PositiveIntegerField()
    status=models.CharField(max_length=20,choices=del_status,default="2")
    date=models.DateTimeField(default=timezone.now())
    order_placed=models.BooleanField(default=0)
    expired=models.BooleanField(default=0)

class product_order(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField()




