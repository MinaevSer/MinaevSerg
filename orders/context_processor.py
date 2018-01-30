from .models import ProductInCart


def gettings_cart_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    products_in_cart = ProductInCart.objects.filter(session_key=session_key)
    products_total_nmb = products_in_cart.count()

    return locals()