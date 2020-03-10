from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

def register(request):
  if request.method == 'POST':
    # Get form values
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    # Check if passwords match
    if password == confirm_password:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username,email=email,password=password)
          
          # Login auto after register
            # auth.login(request, user)
            # messages.success(request, 'You are now logged in')
            # return redirect('index')

          user.save()
          messages.success(request, 'You are now registered and can login')
          return redirect('login')


    else:
      messages.error(request, 'Passwords do not match') 
      return redirect('register')
  else:
    return render(request, 'users/register.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'users/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('/')

def dashboard(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, 'Your account has been updated!')
      return redirect('dashboard')

  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'u_form': u_form,
    'p_form': p_form
  }

  return render(request, 'users/dashboard.html', context)
