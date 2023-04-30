# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.db import connection
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user authentication data to the database
            user = form.save()
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')
            city_id = form.cleaned_data.get('city_id')
            mail_id = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            birthday = form.cleaned_data.get('birthday')
            sex = form.cleaned_data.get('sex')
            weight = form.cleaned_data.get('weight')
            account_creation_date = timezone.now()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO USER_DATA VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                               [username, name, address, city_id, mail_id, phone_number, birthday, sex, weight, account_creation_date])

            password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Correct the errors below')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
