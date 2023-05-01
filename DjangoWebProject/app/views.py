"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest

from.forms import FeedbackForm
from.forms import CommentForm
from.forms import BlogForm
from django.contrib.auth.forms import UserCreationForm

from.models import Blog
from.models import Comment

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts,
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def feedback(request):
    """Renders the feedback page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            GENDER = {
                '1': 'Мужчина',
                '2': 'Женщина',
                '3': 'Другое',
            }
            RATING = {
                '1': 'Плохо',
                '2': 'Нормально',
                '3': 'Хорошо',
                '4': 'Отлично',
                '5': 'Прекрасно',
            }
            data['gender'] = GENDER[form.cleaned_data['gender']]    
            data['rating'] = RATING[form.cleaned_data['rating']]
            if (form.cleaned_data['hasPhone'] == True):
                data['hasPhone'] = 'Да';
            else:
                data['hasPhone'] = 'Нет';
            return render(
                request,
                'app/review.html',
                {
                    'data': data,
                    'title':'Обратная связь',
                    'year':datetime.now().year,
                }
            )
    else:
        form = FeedbackForm()
    return render(
        request,
        'app/pool.html',
        {
            'form': form,
            'title':'Обратная связь',
            'year':datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page"""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            regform.save()
            return redirect('home')
    else:
        regform = UserCreationForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'title': 'Регистрация',
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )