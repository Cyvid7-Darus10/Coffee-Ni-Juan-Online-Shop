from django.db import models
from product.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your models here.

def sort_products(request):
    label = request.GET.get('label')

    sort = request.GET.get('sort')

    # split the sort by '-'
    if sort:
        sort = sort.split('-')
        sort_order = sort[0]
        sort_type = sort[1]

    extra_query = ""

    # get all products from the database
    if label:
        product_list = Product.objects.filter(label__icontains=label)
        extra_query = "&label=" + label
    
    if sort:
        if label:
            product_object = product_list
        else:
            product_object = Product.objects.all()

        if sort_order == "asc":
            product_list = product_object.order_by(sort_type)
            if not label:
                extra_query = "&sort=asc-" + sort_type
        else:
            product_list = product_object.order_by('-' + sort_type)
            if not label:
                extra_query = "&sort=desc-" + sort_type

    if not sort and not label:
        product_list = Product.objects.all()

    # paginate the products
    paginator = Paginator(product_list, 5)
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return product_list, extra_query
