"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from.forms import FeedbackForm

from.forms import CommentForm
from.forms import BlogForm
from django.contrib.auth.forms import UserCreationForm

from.models import Blog, Category, Order, OrderItem, Product
from.models import Comment

from decimal import Decimal

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

def catalog(request):
    categories = Category.objects.all()
    return render(
        request,
        'app/catalog.html',
        {
            'categories': categories,
            'title': 'Каталог',
            'year': datetime.now().year,
        }
    )

def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(
        request,
        'app/category.html',
        {
            'category': category,
            'products': products,
            'year': datetime.now().year,
        }
    )

def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        'app/product.html',
        {
            'product': product,
            'year': datetime.now().year,
        }
    )

def cart(request):
    user = request.user
    try:
        active_order = Order.objects.get(user=user, is_sent=False)
    except Order.DoesNotExist:
        active_order = None
    if active_order:
        cart_items = active_order.order_items.all()
        total_price = sum(item.subtotal for item in cart_items)
    else:
        cart_items = []
        total_price = 0.00
    return render(
        request,
        'app/cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'year': datetime.now().year,
        }
    )

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = 1
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Продукт не найден'}, status=400)
        user = request.user
        active_order, created = Order.objects.get_or_create(user=user, is_sent=False)
        order_item, created = OrderItem.objects.get_or_create(order=active_order, product=product)
        if not created:
            order_item.quantity += quantity
        order_item.save()
        return JsonResponse({'message': 'Продукт добавлен в корзину'})

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            order_item = OrderItem.objects.get(id=item_id)
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Продукт не найден'}, status=400)
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
        return JsonResponse({'message': 'Продукт удалён из корзины'})

def checkout(request):
    user = request.user
    try:
        active_order = Order.objects.get(user=user, is_sent=False)
        active_order.is_sent = True
        cart_items = active_order.order_items.all()
        active_order.total_amount = sum(item.subtotal for item in cart_items) # TO-DO total amount is zero
        active_order.save()
    except Order.DoesNotExist:
        pass
    return render(request, 'app/checkout.html')

def orders(request):
    if request.user.has_perm('app.can_view_all_orders'):
        orders = Order.objects.filter(is_sent=True)
        template_name = 'app/all_orders.html'
    elif request.user.has_perm('app.can_view_orders'):
        orders = Order.objects.filter(user=request.user, is_sent=True)
        template_name = 'app/user_orders.html'
    else:
        orders = None
        template_name = 'app/index.html'
    return render(
        request,
        template_name,
        {
            'orders': orders, 
            'year': datetime.now().year,
        }
    )
