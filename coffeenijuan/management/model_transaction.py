from .models import Transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def sort_transactions(request):
    description = request.GET.get('description')
    
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

    # check if the description is not empty
    if description:
        # get the transactions that match the description
        product_list = Transaction.objects.filter(description__icontains=description)
        extra_query = "?description=" + description
    
    if sort:
        if description:
            product_object = product_list
            extra_query += "&sort="+ sort_order +"-" + sort_type
        else:
            extra_query = "?sort="+ sort_order +"-" + sort_type
            product_object = Transaction.objects.all()

        if sort_order == "asc":
            product_list = product_object.order_by(sort_type)
        else:
            product_list = product_object.order_by('-' + sort_type)

    if not sort and not description:
        product_list = Transaction.objects.all()

    # paginate the transactions
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    
    try:
        transactions = paginator.page(page_number)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return transactions, extra_query


def get_transaction(request, id):
    product = Transaction.objects.get(id=id)
    return product


def get_transactions(request):
    transactions = Transaction.objects.all()
    return transactions