from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy  as _
from django.utils import timezone

user_choices=(
    ("1","customer"),
    ("2","supplier")
)

del_status=(
    ("1","delieverd"),
    ("2","not delieverd")
)
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

class cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

class Product_image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image_link=models.URLField()

class Payment(models.Model):
    id=models.AutoField(primary_key=True)
    
class order(models.Model):
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    del_adress=models.ForeignKey(adress,on_delete=models.DO_NOTHING)
    price=models.PositiveIntegerField()
    taxes=models.PositiveIntegerField()
    discount=models.PositiveIntegerField(default=0)
    final_price=models.PositiveIntegerField()
    status=models.CharField(max_length=20,choices=del_status,default="2")
    date=models.DateTimeField()
    payment_method=models.ForeignKey(Payment,null=True,on_delete=models.SET_NULL)

class product_order(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)





