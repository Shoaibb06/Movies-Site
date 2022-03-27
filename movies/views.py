from django.shortcuts import render, redirect
from .models import *

base_url = 'https://api.themoviedb.org/3/'
def index(request):
    movies = Movie.objects.only('title', 'poster_url')

    return render(request, 'index.html', {'base_url': base_url, 'movies': movies})