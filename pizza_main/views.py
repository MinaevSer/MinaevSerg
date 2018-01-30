from django.shortcuts import render
from django.http import HttpResponse, Http404
from pizzas.models import *
from django.template.loader import render_to_string

# Create your views here.


def home(request):
    tovar = Product.objects.all()
    category_list = Category.objects.all()
    context = {
        'tovars' : tovar,
        'categories' : category_list,
    }
    return render(request, 'index.html', context)


def get_category(request, id):
    try:
        category = Category.objects.get(id = id)
        tovar = Product.objects.filter(category=category)
        category_list = Category.objects.all()
    except:
        raise Http404('Category not found')
    context = {
        'tovars' : tovar,
        'category' : category,
        'categories' : category_list,
    }
    return render(request, 'index_category.html', context)


def item(request, id):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)
    try:
        tovar = Product.objects.get(id=id)
        category_list = Category.objects.all()
    except:
        raise Http404('Object not found')
    context = {
        'tovar' : tovar,
        'categories' : category_list,
    }
    return render(request, 'item.html', context)

def contacts(request):
    category_list = Category.objects.all()
    context = {
        'categories' : category_list,
    }
    return render(request, 'contacts.html', context)
