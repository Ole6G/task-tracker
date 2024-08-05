from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Task, Tag
from .forms import TaskForm
from django.db.models import Q


def task_list(request):
    tasks = Task.objects.all()

    # фильтрация по тегам и статусу выполнения
    tag_filter = request.GET.get('tag')
    status_filter = request.GET.get('status')
    order_by = request.GET.get('order_by')

    if tag_filter:
        tasks = tasks.filter(tags__name=tag_filter)
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'incomplete':
        tasks = tasks.filter(completed=False)

    if order_by:
        tasks = tasks.order_by(order_by)

    # Пагинация
    paginator = Paginator(tasks, 5)  # показывать по 5 задач на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'tag_filter': tag_filter,
        'status_filter': status_filter,
        'order_by': order_by
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
