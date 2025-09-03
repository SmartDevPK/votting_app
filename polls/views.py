# polls/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm  
from django.http import HttpResponse

# Register view
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in after registration
            return redirect("dashboard")  
    else:
        form = SignUpForm()
    return render(request, "polls/register.html", {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return HttpResponse("Invalid username or password")

    return render(request, "polls/login.html")

# Logout view
def logout_view(request):
    logout(request)
    return redirect("login")  # redirect back to login after logout

# Dashboard view (requires login)
@login_required
def dashboard(request):
    return render(request, "polls/dashboard.html")
