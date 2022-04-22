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
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="RING")
    image = models.ImageField(upload_to="images/", null=True, blank=True)    

    def __str__(self):
        return f"{self.title}"

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.ForeignKey(Listing, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("SOLD", "Sold")
    )
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="ACTIVE")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")

    def __str__(self):
        return f"{self.title} by {self.user}"

class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} watched by {self.user}"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0, unique=True)
    title = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default="")
    
    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    comment = models.CharField(max_length=500, default="")
    title = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"{self.comment}"
