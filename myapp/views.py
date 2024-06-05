from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from Authentication.backend import FileBackend
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import os
import json

def post_list(request):
    posts = []
    if os.path.exists('posts.txt'):
        with open('posts.txt', 'r') as f:
            for line in f:
                post = json.loads(line.strip())
                posts.append(post)
    return render(request, 'dashboard.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post_dict = {
                'title': post.title,
                'content': post.content,
                'pk':2
                # Add any other fields you want to include
            }
            with open('posts.txt', 'a') as f:
                f.write(json.dumps(post_dict) + '\n')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            posts = []
            if os.path.exists('posts.txt'):
                with open('posts.txt', 'r') as f:
                    for line in f:
                        post = json.loads(line.strip())
                        if post['id'] == pk:
                            post = form.cleaned_data
                        posts.append(post)
                with open('posts.txt', 'w') as f:
                    for post in posts:
                        f.write(json.dumps(post) + '\n')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_update.html', {'form': form})

@login_required
def post_delete(request, pk):
    if request.method == 'POST':
        posts = []
        if os.path.exists('posts.txt'):
            with open('posts.txt', 'r') as f:
                for line in f:
                    post = json.loads(line.strip())
                    if post['id'] != pk:
                        posts.append(post)
            with open('posts.txt', 'w') as f:
                for post in posts:
                    f.write(json.dumps(post) + '\n')
        return redirect('post_list')
    return render(request, 'post_delete.html', {'post': post})

def home(request):
    return render(request, 'home.html')

import os
import hashlib

def save_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open('credentials.txt', 'a') as f:
        f.write(f'{username},{hashed_password}\n')

def check_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open('credentials.txt', 'r') as f:
        for line in f:
            saved_username, saved_password = line.strip().split(',')
            if saved_username == username and saved_password == hashed_password:
                return True
    return False


def logout_view(request):
    logout(request)
    return redirect('login')

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        auth_backend = FileBackend()  # Create an instance of FileBackend
        user = auth_backend.authenticate(request, username=username, password=password)  # Call the authenticate method on the instance
        if user is not None:
            login(request, user)
        if check_credentials(username, password):
            return render(request, 'dashboard.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        save_credentials(username, password)
        return redirect('home')
    else:
        return render(request, 'registration/register.html')