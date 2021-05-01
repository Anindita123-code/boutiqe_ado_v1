from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Products, Category
from django.db.models import Q
from django.db.models.functions import Lower
from .forms import ProductForm

"""
We can access those url parameters in the all_products view by checking whether request.get exists.
Since we named the text input in the form q. We can just check if q is in request.get
If it is I'll set it equal to a variable called query.If the query is blank it's not going to return any results. So if that's the case let's use
the Django messages framework to attach an error message to the request. And then redirect back to the products url.
We'll also need to import messages, redirect, and reverse up here. In order for that to work and we'll talk more about this later.
If the query isn't blank.I'm going to use a special object from Jango.db.models called Q to generate a search query.
This deserves a bit of an explanation.

In Jango if you use something like product.objects.filter In order to filter a list of products. Everything will be ended together.
In the case of our queries that would mean that when a user submits a query. 
In order for it to match the term would have to appear in both the product name and the product description.
Instead, we want to return results where the query was matched in either
the product name or the description. In order to accomplish this or logic, we need to use Q
This is worth knowing because in real-world database operations.
Queries can become quite complex and using Q is often the only way to handle them.
Because of that, I'd strongly recommend that you become familiar with this and the other complex database functionality.
By reading through the queries portion of the Django documentation. Getting back to the code using Q is actually quite simple
I'll set a variable equal to a Q object. Where the name contains the query. Or the description contains the query.
The pipe here is what generates the or statement. And the i in front of contains makes the queries case insensitive.
With those queries constructed. Now I can pass them to the filter method in order to actually filter the products.
Now I'll add the query to the context. And in the template call it search term.
And we'll start with it as none at the top of this view to ensure we don't get an error when loading the products page without a search term.
"""
# Create your views here.


def all_products(request):
    """ A view to render all the products """
    products = Products.objects.all()

    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']

            sort = sortkey

            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'you didnot enter any search criteria')
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)

            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'
 
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to render individual product """
    product = get_object_or_404(Products, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added product")
            return redirect(reverse('add_product'))
        else:
            messages.error(
                request, "Failed to add product, \
                    please ensure that the form is valid")
    else:
        form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
