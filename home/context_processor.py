from .views import *
from cart.views import *

def home(request):
    categories = Category.objects.all()
    return {'categories':categories}

def cart_details(request):
    total=0
    count=0
    user = request.user

    if user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)

    # check the section have any products
    else:
        cart_id = request.session.get('cart_id')
        cart_items = Cart.objects.filter(cart_id=cart_id)

    item_items = Items.objects.filter(cart__in=cart_items, active=True)
    for i in item_items:
        total += (i.product.price * i.quantity)
        count += i.quantity

    return  {'item_items': item_items, 'total': total, 'count': count}

def searching(request):
    search_word = request.GET.get('search_word', '')
    search_products = []
    no_results_message = None

    if search_word:
        search_products = Product.objects.filter(
            Q(name__icontains=search_word) | Q(description__icontains=search_word),
            available=True
        )
        if not search_products.exists():
            no_results_message = f"No products found matching '{search_word}'."
            print(no_results_message)

    return {
        'search_products': search_products,
        'no_results_message': no_results_message
    }