from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse


def post_list(request):
    if not request.user.is_authenticated:
        return render(request, 'blog/error.html')
    else:
        posts = Post.objects.filter(user_id=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, user_id = request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

from django.contrib import auth

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        auth.login(request, user)
        # Перенаправление на "правильную" страницу
        return HttpResponseRedirect("/post/new/")
        #return HttpResponseRedirect("/error")

    else:
        # Отображение страницы с ошибкой
        return render(request, 'blog/login.html')

def logout(request):
    auth.logout(request)
           # Перенаправление на страницу.
    return render(request, 'blog/logout.html')

def register(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('/post/new/'))
    return render(request, 'blog/register.html', {'form': form})

def error(request):
    return render(request, 'blog/error.html')

