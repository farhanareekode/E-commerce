import uuid

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username is already taken")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email is already taken")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                print("user created")
        else:
            print('password is not correct')
            return redirect('register')

        return redirect('login')
    else:
        return render(request, 'register.html')



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            uid = str(uuid.uuid4())
            request.session['uid'] = uid
            request.session['username'] = username
            return redirect('home')
        else:
            messages.warning(request, 'invalid input')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')