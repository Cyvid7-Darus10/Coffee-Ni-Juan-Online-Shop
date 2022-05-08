from .models import Supply
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SupplyForm, SupplyUpdateForm

# Help Functions

def sort_supplies(request):
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
        # get the supplies that match the label
        supply_list = Supply.objects.filter(label__icontains=label)
        extra_query = "?label=" + label
    
    if sort:
        if label:
            supply_object = supply_list
            extra_query += "&sort="+ sort_order +"-" + sort_type
        else:
            extra_query = "?sort="+ sort_order +"-" + sort_type
            supply_object = Supply.objects.all()

        if sort_order == "asc":
            supply_list = supply_object.order_by(sort_type)
        else:
            supply_list = supply_object.order_by('-' + sort_type)

    if not sort and not label:
        supply_list = Supply.objects.all()

    # paginate the supplies
    paginator = Paginator(supply_list, 5)
    page_number = request.GET.get('page')
    
    try:
        supplies = paginator.page(page_number)
    except PageNotAnInteger:
        supplies = paginator.page(1)
    except EmptyPage:
        supplies = paginator.page(paginator.num_pages)

    return supplies, extra_query

def add_supply_form(request):
    if request.POST:
        form = SupplyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return "redirect"
    else:
        form = SupplyForm()
    
    return form


def delete_supply_item(request, id):
    try:
        Supply.objects.get(id=id).delete()
    except:
        return "error"
    return "success"


def edit_supply_form(request, id):
    supply = get_supply_item(request, id)
    if request.POST:
        form = SupplyUpdateForm(request.POST, request.FILES, instance=supply)
        if form.is_valid():
            form.save()
            return "redirect"
    else:
        form = SupplyUpdateForm(instance=supply)
    
    return form


def get_supply_item(request, id):
    supply = Supply.objects.get(id=id)
    return supply


def get_supply_items(request):
    supplies = Supply.objects.all()
    return supplies