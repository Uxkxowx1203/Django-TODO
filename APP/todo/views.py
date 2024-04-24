from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from user import forms
from .models import Todo, SubTask
from django.core.paginator import Paginator
from todo.forms import TodoForm


@login_required
def todo_list(request):
    todos = Todo.objects.filter(created_by=request.user)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(todos, 5)  # 5 items per page
    page_obj = paginator.get_page(page_number)
    context = {
        'todos': page_obj,
        'paginator': paginator,
        'page_range': paginator.page_range[:5],
    }
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
    return render(request, 'todo_list.html', context)  # Redirect to todo_list after delete for consistency


@login_required
def add_subtask(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, created_by=request.user)

    if request.method == 'POST':
        title = request.POST['title']
        new_subtask = SubTask.objects.create(todo=todo, title=title)
        messages.success(request, 'Subtask added successfully!')
        return redirect('todo_detail', todo_id)
    context = {'todo': todo}
    return render(request, 'add_subtask.html', context)


@login_required
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, pk=subtask_id)
    if request.method == 'POST':
        title = request.POST['title']
        completed = request.POST.get('completed', False)  # Handle checkbox value
        subtask.title = title
        subtask.completed = completed
        subtask.save()
        messages.success(request, 'Subtask edited successfully!')
        return redirect('todo_detail', subtask.todo.id)  # Redirect to todo detail after edit
