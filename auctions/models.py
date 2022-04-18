from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=100, unique=True)
    # slug = models.SlugField(unique=True)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    CATEGORY_CHOICES = (
        ("RING", "Ring"),
        ("BRACELET", "Bracelet"),
        ("NECKLACE", "Necklace"),
        ("EARRINGS", "Earrings"),
        ("PENDANT", "Pendant"),
        ("BROOCH", "Brooch")
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="")
    image = models.ImageField(upload_to="media/images/", null=True, blank=True)    

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
