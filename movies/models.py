from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, null=True)
    overview = models.TextField()
    poster_url = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    duration = models.IntegerField(null=True)
    budget = models.DecimalField(max_digits=30, decimal_places=2, default=0.0)
    revenue = models.DecimalField(max_digits=30, decimal_places=2, default=0.0)
    release_date = models.DateField()
    genres = models.JSONField(null=True)
    video = models.CharField(max_length=50, null=True)
    avg_rating = models.DecimalField(max_digits=30, decimal_places=2, default=0.0)

    def __str__(self):
        return self.title


class User(User):
    address = models.CharField(max_length=200)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='img/')
    coins = models.IntegerField(default=0)

    def _str_(self):
        return self.username


class Rating(models.Model):
    from django.contrib.auth.models import User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def _str_(self):
        return self.rating


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    description = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.description


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    movie_id = models.IntegerField(null=False, blank=False)
