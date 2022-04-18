from django.db import models
from product.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login as auth_login, authenticate
from account.forms import AccountAuthenticationForm
from .forms import inventory_form

# Create your models here.

def sort_products(request):
    label = request.GET.get('label')
    
    sort = request.GET.get('sort')  
    # split the sort by '-'
    # [0] = the order of sorting, "desc" or "asc"
    # [1] = the field to sort by
    if sort:
        sort = sort.split('-')
        sort_order = sort[0]
        sort_type = sort[1]

    # used for double queries
    extra_query = "?"

    # check if the label is not empty
    if label:
        # get the products that match the label
        product_list = Product.objects.filter(label__icontains=label)
        extra_query = "?label=" + label
    
    if sort:
        if label:
            product_object = product_list
            extra_query += "&sort="+ sort_order +"-" + sort_type
        else:
            extra_query = "?sort="+ sort_order +"-" + sort_type
            product_object = Product.objects.all()

        if sort_order == "asc":
            product_list = product_object.order_by(sort_type)
        else:
            product_list = product_object.order_by('-' + sort_type)

    if not sort and not label:
        product_list = Product.objects.all()

    # paginate the products
    paginator = Paginator(product_list, 3)
    page_number = request.GET.get('page')
    
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return products, extra_query



def login_user(request):
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                auth_login(request, user)
                return "redirect"
    else:
        form = AccountAuthenticationForm()
    
    return form


def add_inventory_form(request):
    if request.POST:
        form = inventory_form(request.POST)
        if form.is_valid():
            label       = request.POST['label']
            image_url   = request.POST['image_url']
            price       = request.POST['price']
            stock       = request.POST['stock']
            description = request.POST['description']

            product = Product(label=label, image_url=image_url, price=price, stock=stock, description=description)
            product.save()

            return "redirect"
    else:
        form = inventory_form()
    
    return form

def delete_inventory_item(request, id):
    try:
        Product.objects.get(id=id).delete()
    except:
        return "error"
    return "success"