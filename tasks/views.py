from django.shortcuts import render, redirect, get_object_or_404   # redirect: me redirije segun el nombre que puse en urls, si se busca algo que no esta en la db sale error 404 y no tumbar el servidor

from django.http import HttpResponse            # Para enviar html basicos
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Para traer el template de signup(crear usuario y para comprobar si el usuario existe)
from django.contrib.auth.models import User     # para traer el modelo User
from django.contrib.auth import login, logout, authenticate           # para usar sesiones (abrir y cerrarla), authenticate: para comprobar el username
from django.db import IntegrityError            # marca errores de la db
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
# def helloworld(request):        # request: es lo que envia el usuario
#     #return HttpResponse("Hello World")  # HttpResponse: para dar templates basicos
#     return render(request, "signup.html",{"form": UserCreationForm})   # render: siempre espera el request
# proporciono una vista "UserCreationForm"


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        print("Enviando datos")
        return render(request, "signup.html", {
            "form": UserCreationForm})
    elif request.method == "POST":
        print(request.POST)
        print("Reciviendo datos")
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Registrar usuario
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "El usuario ya existe"})

        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": "Las contrasenhas no coinciden"})

@login_required
def tasks(request):
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull= True)
    return render(request, "tasks.html", {"tasks":tasks})

@login_required
def tasks_completed(request):
    #tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull= False).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks":tasks})

@login_required
def create_tasks(request):
    if request.method == "GET":
        return render(request,"create_task.html",{
            "form": TaskForm
        })
    elif request.method == "POST":
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request,"create_task.html",{
            "form": TaskForm,
            "error": "Ingrese datos validos"
            })

@login_required        
def task_detail(request, task_id):
    if request.method == "GET":
        print(task_id)
        #task = Task.objects.get(pk=task_id)
        task = get_object_or_404(Task,pk=task_id, user= request.user)       # me aseguro que seo solo mis tareas. Si entro a otra tarea me da error 404
        form = TaskForm(instance=task)  # El oformulario se rellena con los valores de "task"
        return render(request, "task_detail.html", {"task" : task, "form" : form})
    elif request.method == "POST":
        try:
            task = get_object_or_404(Task, pk=task_id, user= request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "task_detail.html", {"task" : task, "form" : form, "error": "Error actualizando la tarea"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id, user= request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task,pk=task_id, user= request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    print(request.POST)
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm})
    elif request.method == "POST":
        user = authenticate(
            request, 
            username=request.POST["username"], 
            password=request.POST["password"])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "El usuario o contrasenha esta incorrecta"})
        else:
            login(request, user)
            return redirect("tasks")

