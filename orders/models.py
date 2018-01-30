from django.db import models
from pizzas.models import Product
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=24)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

    def __str__(self):
        return 'Статус %s' % self.name


class Order(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя покупателя')
    phone = models.CharField(max_length=48, default=None, null=True)
    adres = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.name)

    def save(self, *args, **kwargs):
        super(Order, self). save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    nmb = models.IntegerField(default=1, verbose_name='Количество товара в заказе')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    size = models.IntegerField(default=30, verbose_name='Размер(см)')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = "Товары в заказах"

    def __str__(self):
        return '%s' % self.product.name

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        item_category = self.product.category
        item_size = self.size
        self.price = price_per_item
        if item_category.name != "Напитки":
            if int(item_size) < 30:
                self.price = self.price - 125
                self.total_price = int(self.nmb) * (price_per_item-125)
            elif int(item_size) > 30:
                self.price = self.price + 125
                self.total_price = int(self.nmb) * (price_per_item+125)
            else:
                self.total_price = int(self.nmb)*price_per_item
        else:
            self.total_price = int(self.nmb)*price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)
        order = self.order
        all_products_in_order=ProductInOrder.objects.filter(order=order)
        order_total_price = 0
        for item in all_products_in_order:
            order_total_price += item.total_price

        self.order.total_price=order_total_price
        self.order.save(force_update=True)


class ProductInCart(models.Model):
    session_key = models.CharField(max_length=128, editable=False)
    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    nmb = models.IntegerField(default=1, verbose_name='Количество товара в заказе')
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    size = models.IntegerField(default=30, verbose_name='Размер пиццы(диаметр в см)')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = "Товары в корзинах"

    def __str__(self):
        return '%s' % self.product.name

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        item_size = self.size
        item_category = self.product.category
        self.price = price_per_item
        if item_category.name != "Напитки":
            if int(item_size) < 30:
                self.price = self.price - 125
                self.total_price = int(self.nmb) * (price_per_item-125)
            elif int(item_size) > 30:
                self.price = self.price + 125
                self.total_price = int(self.nmb) * (price_per_item+125)
            else:
                self.total_price = int(self.nmb)*price_per_item
        else:
            self.total_price = int(self.nmb)*price_per_item

        super(ProductInCart, self).save(*args, **kwargs)