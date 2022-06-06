from account.models import Account
from .models import add_transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateAccountForm, AccountUpdateForm

# Help Functions

def sort_accounts(request):
    label = request.GET.get('email')
    
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
        # get the supplies that match the label
        account_list = Account.objects.filter(email__icontains=label)
        extra_query = "?email=" + label
    
    if sort:
        if label:
            account_object = account_list
            extra_query += "&sort="+ sort_order +"-" + sort_type
        else:
            extra_query = "?sort="+ sort_order +"-" + sort_type
            account_object = Account.objects.all()

        if sort_order == "asc":
            account_list = account_object.order_by(sort_type)
        else:
            account_list = account_object.order_by('-' + sort_type)

    if not sort and not label:
        account_list = Account.objects.all()

    filter = request.GET.get('filter')

    if filter:
        # get the supplies that match the label
        account_type = filter.split('-')[1]
        account_list = account_list.filter(account_type=account_type)
        extra_query += "&account_type=" + account_type

    # paginate the supplies
    paginator = Paginator(account_list, 5)
    page_number = request.GET.get('page')
    
    try:
        supplies = paginator.page(page_number)
    except PageNotAnInteger:
        supplies = paginator.page(1)
    except EmptyPage:
        supplies = paginator.page(paginator.num_pages)

    return supplies, extra_query

def add_account_form(request):
    if request.POST:
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            add_transaction("Added Account", "Name of Account: {}".format(form.cleaned_data['email']), request.user, form.instance.id)
            return "redirect"
    else:
        form = CreateAccountForm()
    
    return form


def delete_account_item(request, id):
    account = get_account_by_id(request, id)
    try:
        Account.objects.get(id=id).delete()
    except:
        return "error"
    add_transaction("Deleted Account", "Name of Account: {}".format(account.email), request.user, id)
    return "success"


def edit_account_form(request, id):
    account = get_account_by_id(request, id)
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            add_transaction("Edited Account", "Name of Account: {}".format(form.cleaned_data['email']), request.user, form.instance.id)
            return "redirect"
    else:
        form = AccountUpdateForm(instance=account)
    
    return form


def get_account_by_id(request, id):
    account = Account.objects.get(id=id)
    return account


def get_accounts(request):
    supplies = Account.objects.all()
    return supplies