from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,Category
# Create your views here.

def about(request):
    return render(request,'about.html')

def blog(request):
    return render(request,'blog.html')


def product_single(request,category_slug,product_slug):
    product = Product.objects.get(category_id__slug=category_slug,slug=product_slug)
    context = {
        'product':product,
    }
    return render(request,'product-single.html',context)


def home(request, category_slug = None):

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category_id=category).order_by('-date')  # Order by date in descending order
    else:
        products = Product.objects.all().order_by('-date')  # Ensure consistency across pages by ordering

    products = list(products)  # Convert queryset to a list
    random.shuffle(products)

    categories = Category.objects.all()

    # Set up pagination
    show_page = Paginator(products, 4)
    page_num = int(request.GET.get('page', 1))

    try:
        page_product = show_page.page(page_num)
    except (EmptyPage, InvalidPage):
        page_product = show_page.page(show_page.num_pages)

    context={
        'products':products,
        'categories':categories,
        'page_product':page_product
    }
    return render(request,'index.html',context)

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

    return render(request, 'search.html', {
        'search_products': search_products,
        'no_results_message': no_results_message
    })