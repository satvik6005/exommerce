# Generated by Django 4.2.5 on 2023-09-22 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=False, help_text="Active user", verbose_name="active"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="First Name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=254, verbose_name="Last Name"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_email_verified", models.BooleanField(default=False)),
                (
                    "authorization",
                    models.CharField(
                        choices=[("1", "customer"), ("2", "supplier")],
                        default=1,
                        max_length=10,
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.Unselect this instead of deleting accounts.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date created"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "users",
                "ordering": ["-date_created", "email"],
            },
        ),
        migrations.CreateModel(
            name="adress",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("zipcode", models.IntegerField()),
                ("houseno", models.IntegerField()),
                ("locality", models.CharField(max_length=500)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["email"], name="users_user_email_6f2530_idx"),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["first_name", "last_name"], name="users_user_first_n_6d862e_idx"
            ),
        ),
    ]
