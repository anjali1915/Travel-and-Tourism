from django.db import models
from django.conf import settings

class User_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    contact = models.CharField(blank=True, null=True, max_length=255)
    trip_organised = models.TextField(null=True)
    places_visited = models.TextField(null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class User_post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Posted by {self.user.username} on {self.posted_on}"

# Create your models here.
