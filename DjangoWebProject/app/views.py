"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from.forms import FeedbackForm, ProductForm

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
            'title':'Новости',
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
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(
        request,
        'app/category.html',
        {
            'categories': categories,
            'category': category,
            'products': products,
            'year': datetime.now().year,
        }
    )

def product(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        'app/product.html',
        {
            'categories': categories,
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
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)  
        quantity = 1
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Продукт не найден'}, status=400)
        active_order, created = Order.objects.get_or_create(user=user, is_sent=False)
        order_item, created = OrderItem.objects.get_or_create(order=active_order, product=product)
        if not created:
            order_item.quantity += quantity
        order_item.save()
        return JsonResponse({'message': 'Продукт добавлен в корзину'})

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        try:
            item = OrderItem.objects.get(id=item_id)
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Продукт не найден'}, status=400)
        if not (user.has_perm('app.can_view_all_orders') or item.order.user == user):
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        item.delete()
        order_deleted = item.order.update_total_amount()
        return JsonResponse({
            'message': 'Продукт удалён из корзины',
            'order_deleted': order_deleted
        })

def increase_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        try:
            item = OrderItem.objects.get(id=item_id)
            if not (user.has_perm('app.can_view_all_orders') or item.order.user == user):
                return JsonResponse({'error': 'Недостаточно прав'}, status=403)
            item.quantity += 1
            item.save()
            item.order.update_total_amount()
            return JsonResponse({'message': 'Количество увеличено успешно.'})
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Продукт не найден.'})

def decrease_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        try:
            item = OrderItem.objects.get(id=item_id)
            if not (user.has_perm('app.can_view_all_orders') or item.order.user == user):
                return JsonResponse({'error': 'Недостаточно прав'}, status=403)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                item.order.update_total_amount()
                return JsonResponse({'message': 'Количество уменьшено успешно.'})
            else:
                item.delete()
                order_deleted = item.order.update_total_amount()
                return JsonResponse({
                    'message': 'Продукт удален из корзины.',
                    'order_deleted': order_deleted
                })
        except OrderItem.DoesNotExist:
            return JsonResponse({'message': 'Продукт не найден.'})

def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован'}, status=401)
        if not user.has_perm('app.can_view_all_orders'):
            return JsonResponse({'error': 'Недостаточно прав'}, status=403)
        try:
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            return JsonResponse({
                'message': 'Заказ успешно удален.',
                'order_deleted': True
            })
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Заказ не найден.'})

def checkout(request):
    user = request.user
    try:
        active_order = Order.objects.get(user=user, is_sent=False)
        active_order.is_sent = True
        active_order.save()
        active_order.update_total_amount()
    except Order.DoesNotExist:
        pass
    return render(request, 'app/checkout.html')

def orders(request):
    if request.user.has_perm('app.can_view_all_orders'):
        orders = Order.objects.filter(is_sent=True)
        template_name = 'app/all_orders.html'
    elif request.user.is_authenticated:
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

def order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        template_name = 'app/order.html'
    except Order.DoesNotExist:
        pass
    return render(
        request,
        template_name,
        {
            'order': order,
            'year': datetime.now().year,
        }
    )

def add_product(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('catalog')
    else:
        product_form = ProductForm()
    return render(
        request,
        'app/add_product.html',
        {
            'product_form': product_form,
            'title': 'Добавить продукт',
            'year': datetime.now().year,
        }
    )
