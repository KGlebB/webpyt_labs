"""
Definition of models.
"""

from tabnanny import verbose
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    # Методы класса:
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self):
        return self.title
    # Метаданные:
    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Cтатья блога"
        verbose_name_plural = "Cтатьи блога"

admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")
    # Методы класса:
    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)
    # Метаданные:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статье блога"

admin.site.register(Comment)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

admin.site.register(Category)

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Краткое описание")
    content = models.TextField(verbose_name="Полное описание")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

admin.site.register(Product)

class OrderStatus(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название статуса")
    color = models.CharField(max_length=10, verbose_name="Фоновый цвет статуса")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"

admin.site.register(OrderStatus)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма", default=0.00)
    is_sent = models.BooleanField(default=False, verbose_name="Заказ отправлен")
    status = models.ForeignKey(OrderStatus, default=1, on_delete=models.SET_DEFAULT, verbose_name="Статус")

    def update_total_amount(self):
        total_amount = self.order_items.aggregate(sum=models.Sum('subtotal'))['sum'] or 0.00
        self.total_amount = total_amount
        if total_amount == 0.00:
            self.delete()
            return True
        else:
            self.save()
            return False

    def __str__(self):
        return f"Заказ #{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        permissions = [
            ("can_make_orders", "Can make orders"),
            ("can_view_orders", "Can view orders"),
            ("can_view_all_orders", "Can view all orders"),
        ]

admin.site.register(Order)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    def save(self, *args, **kwargs):
        # Calculate the subtotal for the order item.
        self.subtotal = self.product.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

admin.site.register(OrderItem)