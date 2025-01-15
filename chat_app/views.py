# chat_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.http import HttpResponseRedirect
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'home.html', {'users': users})

@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
        return HttpResponseRedirect(reverse('chat', args=[username]))

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')
    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages,
        'users': User.objects.exclude(id=request.user.id),
    })