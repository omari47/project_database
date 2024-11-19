
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from sacco_app.app_forms import CustomerForm, DepositForm, LoginForm
from sacco_app.models import Customer, Deposit


# Create your views here.
def test(request):
    # save a customer
    # c1 = Customer(first_name = 'John', last_name = 'Smith', email='smith@gmail.com', dob='2000-11-28', gender='Male', weight=62)
    # c1.save()
    # c2 = Customer(first_name='John', last_name='Smith', email='mercy@gmail.com', dob='2002-11-28', gender='Female',
    #               weight=56)
    # c2.save()
    count = Customer.objects.count()

    c1 = Customer.objects.get(id=1)
    print(c1)
    return HttpResponse(f"Ok, Done, We have {customers} customers")


def customers(request):
    data = Customer.objects.all().order_by('-id').values()# ORM select * from customers
    paginator = Paginator(data, 15)
    page = request.GET.get('page', 1)
    try:
      paginated_data = paginator.page(page)
    except  EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, "customers.html", {"data": paginated_data})


def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id) # select * from customers where id=7
    customer.delete() # delete from customers where id=7
    return redirect('customers')






def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, f"Customer {form.cleaned_data['first_name']} was added!")
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {"form": form})


def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            # messages.success(request, f"Customer {form.cleaned_data['first_name']} was updated!")
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_update_form.html', {"form": form})



def details_customer(request,customer_id):
    customer = Customer.objects.get(id=customer_id)
    deposits = customer.deposits.all()
    return render(request, 'details.html', {'customer': customer, 'deposits': deposits})


def search_customer(request):
    search_term = request.GET.get('search')
    data = Customer.objects.filter(
        Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term) | Q(email__icontains=search_term))
     # ORM select * from customers
    paginator = Paginator(data, 15)
    page =  1# data = Customer.objects.all().order_by('-id').values()request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page)
    except  EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, "customers.html", {"data": paginated_data})

def deposit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    deposits = customer.deposits.all() # foregin key relationship
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            depo = Deposit(amount=amount, status=True, customer=customer)
            depo.save()
            # messages.success(request, 'Your deposit has been successfully saved')
            return redirect('customers')
    else:
        form = DepositForm()
    return render(request, 'deposit_form.html', {"form": form, "customer": customer})



def login_user(request):
    form = LoginForm()
    return render(request, "login_form.html",{"form": form})


def logout_user(request):
    return None


#
# pip install django-crispy-forms
# pip install crispy-bootstrap5
# pip install Pillow