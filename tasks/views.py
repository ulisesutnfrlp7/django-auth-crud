# tasks/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import CreateNewTask, UpdateTask
from .models import Task
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        context = {
        'form': UserCreationForm()
        }
        return render(request, 'signup.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user) # esto sirve para iniciar sesión automáticamente después de registrarse. es importante porque si no lo hacemos, el usuario tendría que iniciar sesión manualmente después de registrarse, lo cual no es una buena experiencia de usuario.
                return redirect('tasks')
            except IntegrityError:
                context = {
                    'form': UserCreationForm(),
                    'error': 'Username already exists'
                }
                return render(request, 'signup.html', context)
        context = {
            'form': UserCreationForm(),
            'error': 'Passwords do not match'
        }
        return render(request, 'signup.html', context)


@login_required
def tasks(request):
    show_completed = request.GET.get('show_completed')  # viene del checkbox
    show_pending = request.GET.get('show_pending')  # viene del checkbox
    # aca se listarán las tareas del usuario logueado. para eso, primero tenemos que obtener el usuario logueado y luego filtrar las tareas por ese usuario.
    if show_completed:
        tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    elif show_pending:
        tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    else:
        tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks
    }
    # si el usuario todavia no se logueo, entonces no se le mostrará ninguna tarea, porque el filtro no encontrará ninguna tarea que tenga un usuario asociado. pero si el usuario se loguea, entonces se le mostrarán todas las tareas que tenga asociadas a su cuenta.
    return render(request, 'tasks.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('home')

# def signin(request):
    if request.method == 'GET':
        context = {
        'form': AuthenticationForm()
        }
        return render(request, 'signin.html', context)
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context = {
                'form': AuthenticationForm(),
                'error': 'Username and password do not match'
            }
            return render(request, 'signin.html', context)
        else:
            login(request, user)
            return redirect('tasks')

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

@login_required
def create_task(request):
    if request.method == 'GET':
        context = {
            'form': CreateNewTask()
        }
        return render(request, 'create_task.html', context)
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

@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.datecompleted = timezone.now() # asignamos la fecha actual
        task.save()
        return redirect('tasks') # redirige a la lista de tareas

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # necesito que el formulario ya venga rellenado con los datos de la tarea, para eso, tengo que crear un diccionario con los datos de la tarea y pasarlo al formulario.
        form = UpdateTask(initial={
            'title': task.title,
            'description': task.description,
            'important': task.important,
            'completed': task.datecompleted is not None
        })
        context = {
            'task': task,
            'form': form
        }
        return render(request, 'task_detail.html', context)
    else: # sino, la tarea se actualiza con los datos del formulario y se redirige a la lista de tareas.
        task = get_object_or_404(Task, pk=task_id, user=request.user)
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
        print(request.POST)
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')