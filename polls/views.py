# polls/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm  
from django.contrib.auth.decorators import login_required

# Register view
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")  
    else:
        form = SignUpForm()
    return render(request, "polls/register.html", {"form": form})

# Dashboard view (requires login)
@login_required
def dashboard(request):
    return render(request, "polls/dashboard.html")  

# Logout view
def logout_view(request):
    logout(request)
    return redirect("register")  
