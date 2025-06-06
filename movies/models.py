from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

class Movie(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='movies'
    )
    title = models.CharField(max_length=255)
    rate = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )  # e.g. 1 to 10
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"