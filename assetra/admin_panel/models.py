from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models

from .helper import format_mobile, get_country_name


class User(AbstractUser):
    country = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    verified = models.BooleanField(default=False)
    profile = models.ImageField(upload_to="profile/", null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": (f"{self.first_name} {self.last_name}"),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile": format_mobile(self.mobile),
            "dob": self.dob.strftime("%b %d %Y") if self.dob else None,
            "country": get_country_name(self.country),
            "date_joined": (
                self.date_joined.strftime("%b %d %Y, %I:%M %p")
                if self.date_joined
                else None
            ),
            "verified": self.verified,
            "profile": self.profile.url if self.profile else None,
        }


class Referral(models.Model):
    referred_by = models.ForeignKey(
        User, related_name="referrals", on_delete=models.CASCADE
    )
    referred_user = models.OneToOneField(
        User, related_name="referred", on_delete=models.CASCADE
    )
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referred_by.username} referred {self.referred_user.username}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    cover_image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", related_name="posts", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate slug if not already set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
