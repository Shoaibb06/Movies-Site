from django.urls import path

from . import views

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/',views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_user/<int:user_id>', views.edit_user, name='edit_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password')

]