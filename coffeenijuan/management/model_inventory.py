from product.models import Product
from .models import add_transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import InventoryForm, InventoryUpdateForm


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
    paginator = Paginator(product_list, 5)
    page_number = request.GET.get('page')
    
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return products, extra_query


def add_inventory_form(request):
    if request.POST:
        form = InventoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            add_transaction("Added Inventory", "Name of Product: {}".format(form.cleaned_data['label']), request.user, form.instance.id)
            return "redirect"
    else:
        form = InventoryForm()
    
    return form


def delete_inventory_item(request, id):
    product = get_inventory_item(request, id)
    try:
        Product.objects.get(id=id).delete()
    except:
        return "error"
    add_transaction("Deleted Supply", "Name of Supply: {}".format(product.label), request.user, id)
    return "success"


def edit_inventory_form(request, id):
    product = get_inventory_item(request, id)
    if request.POST:
        form = InventoryUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            add_transaction("Edited Product", "Name of Product: {}".format(form.cleaned_data['label']), request.user, form.instance.id)
            return "redirect"
    else:
        form = InventoryUpdateForm(instance=product)
    
    return form


def get_inventory_item(request, id):
    product = Product.objects.get(id=id)
    return product


def get_inventory_items(request):
    products = Product.objects.all()
    return products