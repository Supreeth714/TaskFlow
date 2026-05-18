from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    q = request.GET.get('q','')
    status = request.GET.get('status','')
    tasks = Task.objects.filter(owner=request.user)
    if q: tasks = tasks.filter(title__icontains=q)
    if status: tasks = tasks.filter(status=status)
    return render(request, 'tasks/task_list.html', {'tasks':tasks,'q':q,'status':status})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False); t.owner = request.user; t.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form':form,'title':'New Task'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form':form,'title':'Edit Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete(); return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task':task})

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.status = 'done' if task.status != 'done' else 'todo'
    task.save()
    return redirect('task_list')
