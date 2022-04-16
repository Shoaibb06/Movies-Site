from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from django.conf import settings
from django.core.mail import send_mail
from movies.models import User
import string
import random


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Username or or passsword is incorrect, Try again..!')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You were logged out!')
    return redirect('index')


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "You have been successfully registered!")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'authenticate/register.html', {'form': form})

    else:
        form = UserRegistrationForm()
        return render(request, 'authenticate/register.html', {'form': form})


@login_required
def edit_user(request, user_id):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.profile_picture = form.cleaned_data['profile_picture']
            user.save()
            messages.success(request, "Profile updated Successfully!")
            return render(request, 'authenticate/edit_profile.html',
                          {'form': form, 'current_user': user, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})
    else:
        if user:
            form = UserUpdateForm(request.POST or None, instance=user)
            return render(request, 'authenticate/edit_profile.html',
                          {'form': form, 'current_user': user, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})
        else:
            return render(request, '404_page.html')


# from django.contrib.auth.models import User
@login_required
def change_password(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        password = request.POST.get('password1')
        c_password = request.POST.get('password2')
        if password == c_password:
            user.set_password(password)
            user.save(update_fields=['password'])
        else:
            messages.error(request, "Password is not same in both fields")
            return redirect('change_password')
        return redirect('edit_user', user_id=user.id)
    else:
        return render(request, 'authenticate/update_password.html', {})


def forgot_password(request):
    if request.method == 'POST':
        subject = 'Password'
        user = User.objects.filter(email=request.POST.get('email'))
        letters = string.ascii_lowercase
        password = (''.join(random.choice(letters) for i in range(10)))

        if user:
            user = user[0]
            user.set_password(password)
            user.save()
            message = f'Hi {user.first_name}, Here is your Password.\nPassword: { password }'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list )
            messages.success(request, 'Email containing password sent successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Error! User does not exist')
            return render(request, 'authenticate/forgot_password.html', {})
    else:
        return render(request, 'authenticate/forgot_password.html', {})
