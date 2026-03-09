# tasks/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import CreateNewTask, UpdateTask
from .models import Task
from django.utils import timezone

# Home
def home(request):
    return render(request, 'home.html')

# Signup
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # inicia sesión automáticamente
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Invalid signup data'
            })

# Signin
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html', {
                'form': form,
                'error': 'Username and password do not match'
            })

# Logout
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# Tasks list
@login_required
def tasks(request):
    show_completed = request.GET.get('show_completed')
    show_pending = request.GET.get('show_pending')

    if show_completed:
        tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    elif show_pending:
        tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    else:
        tasks = Task.objects.filter(user=request.user)

    return render(request, 'tasks.html', {'tasks': tasks})

# Create task
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': CreateNewTask()})
    else:
        form = CreateNewTask(request.POST)
        if form.is_valid():
            Task.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                important=form.cleaned_data['important'],
                user=request.user
            )
            return redirect('tasks')

# Complete task
@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

# Task detail & update
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = UpdateTask(initial={
            'title': task.title,
            'description': task.description,
            'important': task.important,
            'completed': task.datecompleted is not None
        })
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        form = UpdateTask(request.POST)
        if form.is_valid():
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.important = form.cleaned_data['important']
            if not form.cleaned_data['completed'] and task.datecompleted is not None:
                task.datecompleted = None
            else:
                task.datecompleted = timezone.now()
            task.save()
        return redirect('tasks')

# Delete task
@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')