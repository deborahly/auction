from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
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
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title}"

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed")
    )
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="ACTIVE")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")

    def __str__(self):
        return f"{self.listing} by {self.user}"

class Watching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing} watched by {self.user}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2, default="")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default="")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.bid} by {self.user}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return "Comment {} by {}".format(self.body, self.user)