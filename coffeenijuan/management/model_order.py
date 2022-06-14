import email
from payment.models import Order, Payment
from account.models import Account
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def sort_orders(request):
    customer = request.GET.get('customer')
    
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
    if customer:
        customers = order.objects.filter(email__icontains=customer)
        order_list = Order.objects.filter(customer__in=customers)
        extra_query = "?customer=" + customer
    
    if sort:
        if customer:
            product_object = order_list
            extra_query += "&sort="+ sort_order +"-" + sort_type
        else:
            extra_query = "?sort="+ sort_order +"-" + sort_type
            product_object = Order.objects.all()

        if sort_order == "asc":
            order_list = product_object.order_by(sort_type)
        else:
            order_list = product_object.order_by('-' + sort_type)

    if not sort and not customer:
        order_list = Order.objects.all()

    filter = request.GET.get('filter')

    if filter:
        # get the supplies that match the label
        filter_type = filter.split('-')
        if filter_type[0] == "payment_type":
            filtered_order_list = []
            for order in order_list:
                if order.payment.payment_option == filter_type[1]:
                    filtered_order_list.append(order)
            order_list = filtered_order_list
        elif filter_type[0] == "status_type":
            order_list = order_list.filter(status=filter_type[1])
        extra_query += ("&" + filter)

    # paginate the order
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    
    try:
        order = paginator.page(page_number)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)

    return order, extra_query


def update_order_status(request, id, status):
    try:
        order = Order.objects.get(id=id)
        order.status = status
        order.save()
    except:
        return 'error'

    return 'success'


def get_order_by_id(request, id):
    product = Order.objects.get(id=id)
    return product


def get_all_order(request):
    order = Order.objects.all()
    return order