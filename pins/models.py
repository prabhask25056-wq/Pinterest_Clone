from django.db import models
from django.conf import settings
# Create your models here.
class Pin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='pins')
    title= models.CharField(max_length=150)
    description= models.TextField(blank=True)
    image_url = models.URLField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title