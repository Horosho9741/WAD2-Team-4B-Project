from time import timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    views = models.IntegerField(default=0)
    icon = models.CharField(max_length=64, default='')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    uid = models.IntegerField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.99)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=16)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "Order"

class Review(models.Model):
    title = models.CharField(max_length=32)
    review = models.TextField(max_length=225)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.review

class Order(models.Model):
    uid = models.CharField(unique=True, default='', max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    time_ordered = models.DateTimeField(default=timezone.now)
    arrival_time = models.DateTimeField(default=timezone.now)
