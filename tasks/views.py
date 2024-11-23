from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UserInviteForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm



@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    invite_form = UserInviteForm()

    if request.method == 'POST':
        invite_form = UserInviteForm(request.POST)
        if invite_form.is_valid():
            invite_form.send_invitation()
            messages.success(request, "Invitation sent successfully!")
            return redirect('task_list')

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'invite_form': invite_form,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('task_list')

# @login_required
# def invite_user(request):
#     if request.method == 'POST':
#         form = UserInviteForm(request.POST)
#         if form.is_valid():
#             form.send_invitation()  # Call the method to handle the invitation email logic
#             return redirect('invite_success')  # Redirect to a valid success page
#     else:
#         form = UserInviteForm()

#     return render(request, 'invite_user.html', {'form': form})


# @login_required
# def success_view(request):
#     return render(request, 'success.html', {'message': 'Invitation sent successfully!'})

# accounts/views.py


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})


