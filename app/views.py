from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from app.models import Budget, BudgetItem, Client

from .forms import (BudgetItemForm, BudgetItemSearchForm, ClientForm,
                    LoginForm, SelectClientForm)
from .utils import render_template


def home(request):
    return render(request, 'home.html')

@login_required
def history(request):
    budget_id = None
    if request.method == 'GET':
        form = BudgetItemSearchForm(request.GET)
        if form.is_valid():
            budget_id = form.cleaned_data.get('budget_id')
    else:
        form = BudgetItemSearchForm()

    if budget_id:
        context_items = Budget.objects.filter(budget_id=budget_id)
    else:
        context_items = Budget.objects.all()

    paginator = Paginator(context_items, 10)  # Mostra 10 orçamentos por página
    page = request.GET.get('page')
    try:
        context_items = paginator.page(page)
    except PageNotAnInteger:
        context_items = paginator.page(1)
    except EmptyPage:
        context_items = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'context_items': context_items, 'budget_item_search_form': form})

@login_required
def budget_detail(request, budget_id):
    context = Budget.objects.get(budget_id=budget_id)

    return render(request, 'detail.html', {'context': context})

@login_required
def render_pdf(request, budget_id):
    context = get_object_or_404(Budget, budget_id=budget_id)
    data = {'client': context.client, 'date': context.date_time}
    output_svg, pdf_file = render_template(data, context.items.all())

    with open(pdf_file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{context.budget_id}.pdf"'
        return response

@login_required
def budget_submit(request, budget_id=None):
    if budget_id:
        budget = Budget.objects.get(budget_id=budget_id)
    else:
        budget = None

    if request.method == 'POST':
        select_client_form = SelectClientForm(request.POST)
        context_form = BudgetItemForm(request.POST)
        if select_client_form.is_valid() and context_form.is_valid():
            client = select_client_form.cleaned_data['client']
            if not budget:
                budget = Budget.objects.create(client=client)
            budget_item = context_form.save(commit=False)
            budget_item.budget = budget
            budget_item.client = client
            budget_item.save()
            if 'save_add_new' in request.POST:
                return redirect('budget_submit', budget_id=budget.budget_id)
            else:
                output_svg, pdf_file = render_template({'client': client, 'date': budget.date_time}, budget.items.all())
                return render(request, 'result.html', {'client': client, 'context': budget.items.all(), 'output_svg': output_svg, 'pdf_file': pdf_file})
    else:
        select_client_form = SelectClientForm()
        context_form = BudgetItemForm()

    return render(request, 'form.html', {'select_client_form': select_client_form, 'context_form': context_form})

@login_required
def client_view(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client_form.save()

            return redirect('client_view')
    elif request.method == 'GET':
        clients = Client.objects.all()

        return render(request, 'client.html', {'clients': clients})
    else:
        client_form = ClientForm()

    return render(request, 'client.html', {'client_form': client_form})

@login_required
def client_create(request, client_id=None):
    if client_id:
        client = get_object_or_404(Client, id=client_id)
    else:
        client = None

    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            return HttpResponseRedirect(reverse('client_view'))
    else:
        client_form = ClientForm(instance=client)
    return render(request, 'client_create.html', {'client_form': client_form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                form.add_error(None, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)

    # return render(request, 'logout.html')
    return redirect('home')

def budget_formset(request):
    formset = formset_factory(BudgetItemForm, can_delete=True, extra=1)
    if request.method == 'POST':
        select_client_form = SelectClientForm(request.POST)
        budget_item_formset = formset(request.POST)
        if select_client_form.is_valid() and formset.is_valid():
            # faz o que precisa, salva o budgetitem
            new_items = []
            for budget_item_form in budget_formset:
                new_items.append(BudgetItem(**budget_item_form.cleaned_data))
    else:
        select_client_form = SelectClientForm()
        budget_item_formset = formset()

    return render(request, 'formset.html', {'select_client_form': select_client_form, 'budget_item_formset': budget_item_formset})

def create_budget_item(request):
    form = BudgetItemForm()
    context = {'form': form}

    return render(request, 'partials/budget_item_form.html', context)

def foo(request):
    form = BudgetItemForm()
    context = {'form': form}

    if request.method == 'POST':
        pass

    return render(request, 'partials/form.html', context)