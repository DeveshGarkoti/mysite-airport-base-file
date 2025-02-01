from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm  # Create a form for your comment model

def register(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home or another page
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home or another page
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('home')



@login_required 
def add_comment(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    model = content_type.model_class()
    obj = get_object_or_404(model, id=object_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = content_type
            comment.object_id = obj.id
            comment.save()
            return redirect(obj.get_absolute_url())  # Redirect to the object's detail page

    # If the form is invalid, redirect back to the detail view or handle the error
    return redirect(obj.get_absolute_url())
