from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import SignUpForm, PollForm
from .models import Poll, Choice


# -----------------------------
# User Authentication Views
# -----------------------------

def register(request):
    """
    Handle user registration
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "polls/register.html", {"form": form})


def login_view(request):
    """
    Handle user login
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("add_poll")  # Redirect to add_poll page after login
        else:
            return HttpResponse("Invalid username or password")

    return render(request, "polls/login.html")


def logout_view(request):
    """
    Handle user logout
    """
    logout(request)
    return redirect("login")


# -----------------------------
# Poll Management Views
# -----------------------------

@login_required
def dashboard(request):
    """
    Display all polls with their choices
    """
    polls_with_choices = Poll.objects.prefetch_related('choice_set').all()
    return render(request, "polls/dashboard.html", {'polls_with_choices': polls_with_choices})


@login_required
def add_poll(request):
    """
    Add a new poll with multiple choices
    """
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)  # Don't save to DB yet

            # Handle created_at if present
            if hasattr(poll, 'created_at') and isinstance(poll.created_at, str):
                try:
                    poll.created_at = datetime.strptime(poll.created_at, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    poll.created_at = datetime.now()
            else:
                if hasattr(poll, 'created_at'):
                    poll.created_at = datetime.now()

            poll.save()  # Save poll to DB

            # Save all non-empty choices
            choice_texts = request.POST.getlist('choice_text')
            for text in choice_texts:
                if text.strip():  # ignore empty fields
                    Choice.objects.create(poll=poll, choice=text, votes=0)

            return redirect('dashboard')  # Redirect to dashboard after saving

    else:
        poll_form = PollForm()

    return render(request, "polls/add_poll.html", {'poll_form': poll_form})
