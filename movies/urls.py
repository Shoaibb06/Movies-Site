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
    path('genres', views.genres, name='genres'),
    path('movie_list/<str:genre>', views.movie_list, name='movie_list'),
    path('movie_details/<int:movie_id>', views.movie_details, name='movie_details'),

    # payment
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('create_checkout_session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
]
