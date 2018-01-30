from django.shortcuts import render
from django.http import JsonResponse
from .models import ProductInCart, Order, ProductInOrder
from pizzas.models import Category
from .forms import CheckForm


def cart_add(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    size = data.get("size")
    is_delete = data.get("is_delete")

    if is_delete:
        ProductInCart.objects.filter(id=product_id).delete()
    else:
        new_product, created = ProductInCart.objects.get_or_create(size=size, session_key=session_key, product_id=product_id, defaults={"nmb" : nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProductInCart.objects.filter(session_key=session_key)
    products_total_nmb = products_in_basket.count()

    return_dict["products_total_nmb"] = products_total_nmb
    return JsonResponse(return_dict)


def cart_page(request):
    session_key = request.session.session_key
    items = ProductInCart.objects.filter(session_key=session_key)
    category_list = Category.objects.all()
    form = CheckForm(request.POST or None)
    context = {
        'items' : items,
        'categories' : category_list,
        'form' : form,
    }
    if request.POST:
        if form.is_valid():
            print(request.POST)
            data = request.POST
            name = data.get("name")
            phone = data["phone"]
            adres = data["adres"]
            order = Order.objects.create(name=name, adres=adres, phone=phone, status_id=2)
            for item in items:
                item_name=item.product
                item_nmb = int(item.nmb)
                item_total_price = item.total_price
                item_price = item.price
                order = order
                item_size = item.size
                ProductInOrder.objects.create(product = item_name, nmb = item_nmb, price = item_price, total_price = item_total_price, order=order, size = item_size)
                ProductInCart.objects.filter(session_key=session_key).delete()
        else:
            print('error')

    return render(request, 'cart.html', context)