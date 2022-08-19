from django.shortcuts import render, redirect
from .models import Post
from django.urls import reverse_lazy

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, 
DeleteView, FormView)

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class LogIn(LoginView):
    model = Post
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('posts')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts')
        return super(RegisterPage, self).get(*args, **kwargs)


class PostList(ListView, LoginRequiredMixin):
    model = Post
    context_object_name = 'posts'


class PostDetail(DetailView, LoginRequiredMixin):
    model = Post


class PostCreate(CreateView, LoginRequiredMixin):
    model = Post
    fields = ['body']
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView, LoginRequiredMixin):
    model = Post
    fields = ['body']
    template_name = 'base/post_update.html'
    success_url = reverse_lazy('posts')


class PostDelete(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('posts')