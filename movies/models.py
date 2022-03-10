from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Movie(models.Model):
    GENRE_CHOICES = [('AC', 'Action'), ('AD', 'Adventure'), ('AN', 'Animation'), ('BI', 'Biography'), ('CO', 'Comedy'),
                     ('DO', 'Documentary'), ('DR', 'Drama'), ('FA', 'Family'), ('HI', 'History'), ('HO', 'Horror'),
                     ('MY', 'Mystery'), ('RO', 'Romance'), ('TH', 'Thriller'), ('WA', 'War')]
    LANGUAGE_CHOICES = [('EN', 'English'), ('FR', 'French'), ('GE', 'German'), ('RU', 'Russian')]
    STATUS_CHOICES = [('RA', 'Recently Added'), ('MW', 'Most Watched'), ('TR', 'Top Rated')]
    title = models.CharField(max_length=100)
    storyline = models.TextField()
    poster = models.ImageField(upload_to='movies')
    genre = models.CharField(choices=GENRE_CHOICES, max_length=2)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)
    director = models.CharField(max_length=100)
    duration = models.TimeField()
    release_date = models.DateField()

    def __str__(self):
        return self.title


class User(User):
    address = models.CharField(max_length=200)

    def _str_(self):
        return self.username


class Ratings(models.Model):
    rating = models.IntegerField()

    def _str_(self):
        return self.rating


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    description = models.TextField()


review_date = models.DateTimeField()


def _str_(self):
    return self.review_comments
