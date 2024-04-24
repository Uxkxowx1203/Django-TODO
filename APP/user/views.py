from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from user import forms
from .models import Todo, SubTask
from django.core.paginator import Paginator
from .forms import TodoForm


@login_required
def profile(request):
    print(dir(request.user))
    context = {
    'username': request.user,
    'first_name': request.user.first_name,
    'email': request.user.email,
    'last_login': request.user.last_login,
    'date_joined': request.user.date_joined,
    }
    return render(request, 'profile.html', context)


def welcome(request):
    return render(request,'welcome.html')


def SignUP(request):
    form = forms.myform()
    if request.method == 'POST':
        form = forms.myform(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/signin')
        else:
            print(form.errors)
    return render(request,'registeration.html',{'form':form})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/signin')


def Sign_in(request):
    if request.method == "POST":
        name = request.POST['un']
        pswd = request.POST['pwd']
        user = authenticate(username=name, password=pswd)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/profile')
        else:
            wrngpass=("Sorry!! You are not authenticated!!! please check your User Name And Password")
            return render(request,'login.html',{'wrngpass':wrngpass})
    return render(request,'login.html')


@login_required
def todo_list(request):
    todos = Todo.objects.filter(created_by=request.user)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(todos, 5)  
    page_obj = paginator.get_page(page_number)
    context = {
        'todos': page_obj, 
        'paginator': paginator,  
        'page_range': paginator.page_range[:5],
    }
    print(context)
    return render(request, 'todo_list.html', context)


def todo_detail(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    subtasks = todo.subtasks.all()
    context = {'todo': todo, 'subtasks': subtasks}
    return render(request, 'todo_detail.html', context)


@login_required
def add_todo(request):
  if request.method == 'POST':
    form = TodoForm(request.POST) 
    if form.is_valid():
      new_todo = form.save(commit=False)  
      new_todo.created_by = request.user  
      new_todo.save()
      messages.success(request, 'Todo added successfully!')  
      return HttpResponseRedirect('/todo_list') 
  else:
    form = TodoForm() 
  context = {'form': form}
  return render(request, 'add_todo.html', context)


@login_required
def edit_todo(request, todo_id):
  todo = get_object_or_404(Todo, pk=todo_id)
  if request.method == 'POST':
    form = TodoForm(request.POST, instance=todo)  
    if form.is_valid():
      form.save()  
      messages.success(request, 'Todo edited successfully!')
      return HttpResponseRedirect('/todo_list') 
  else:
    form = TodoForm(instance=todo)  
  context = {'form': form, 'todo': todo}
  return render(request, 'edit_todo.html', context)


@login_required
def delete_todo(request, todo_id):
  todo = get_object_or_404(Todo, pk=todo_id)
  if request.method == 'POST':
    todo.delete()
    messages.success(request, 'Todo deleted successfully!')
    return HttpResponseRedirect('/todo_list') 
  context = {'todo': todo}
  return render(request, 'todo_list.html', context)  


@login_required
def add_subtask(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, created_by=request.user)
    
    if request.method == 'POST':
        title = request.POST['title']
        new_subtask = SubTask.objects.create(todo=todo, title=title)
        return redirect('todo_detail', todo_id)
    context = {'todo': todo}
    return render(request, 'add_subtask.html', context)


@login_required
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, pk=subtask_id)
    if request.method == 'POST':
        title = request.POST['title']
        completed = request.POST.get('completed', False)  
        subtask.title = title
        subtask.completed = completed
        subtask.save()
        return redirect('todo_detail', subtask.todo.id)  
    context = {'subtasks': [subtask]}  
    return render(request, 'edit_subtask.html', context)


@login_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, pk=subtask_id)
    todo_id = subtask.todo.id  
    subtask.delete()
    return redirect('todo_detail', todo_id)


def update_subtask(request, subtask_id):
  if request.method == 'POST':
    subtask = get_object_or_404(SubTask, pk=subtask_id)
    subtask.completed = not subtask.completed  
    subtask.save()
  return redirect('todo_detail', todo_id=subtask.todo.id) 


def update_todo(request, todo_id):
  todo = Todo.objects.get(pk=todo_id)
  if request.method == 'POST':
    todo.completed = request.POST.get('completed', False) 
    return redirect('todo_list')  
  context = {'todo': todo}
  return render(request, 'todo_detail.html', context) 