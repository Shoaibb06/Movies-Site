"""movies_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # payment
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('create_checkout_session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),

    path('submit-rating/', views.submit_rating, name='submit_rating'),
    path('genres/', views.genres, name='genres'),
    path('movie_list/<str:genre>/', views.movie_list, name='movie_list'),
    path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('search/', views.search, name='search'),
    path('add_review/', views.add_review, name='add_review'),
    path('by_rating/', views.by_rating, name='by_rating'),
    path('most_recent/', views.most_recent, name='most_recent'),
    path('old_movies/', views.old_movies, name='old_movies'),
    path('movie_overview/<int:movie_id>/', views.movie_overview, name='movie_overview'),
    path('add_to_playlist/<int:movie_id>/', views.add_to_playlist, name= 'add_to_playlist'),
    path('show_playlist', views.show_playlist, name= 'show_playlist')
]
