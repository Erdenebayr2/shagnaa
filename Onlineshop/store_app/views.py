from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from accounts.models import Account
from django.core.paginator import Paginator
import sqlite3
from django.db import transaction
from django.views.decorators.http import require_http_methods
from transliterate import translit
from carts_app.models import CartItem
from carts_app.views import _cart_id
from django.db.models import Q
from django.views.decorators.http import require_POST
import sqlite3 as sql
from django.contrib.auth.models import User
from .form import *
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib import messages
from .form import DriverForm, TrailerForm, TrailerFileForm, ApplicationForm
from .models import Product, ImageGallery, User_Request,UserRequest_Truck
from django.contrib.auth.decorators import login_required
from datetime import datetime

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']
    
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        
        news = News(title=title, description=description, image=filename)
        news.save()
        
        return redirect('a')
    
    return render(request, 'admin/add_news.html')

def handle_upload(a_img, name):
    if a_img:
        with open(name, 'wb+') as destination:
            for chunk in a_img.chunks():
                destination.write(chunk)

def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('-id')[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, "index.html", context)

def base(request):
    return render(request, "base.html")

def dashboard(request):
    return render(request, "dashboard.html")

def order_complete(request):
    return render(request, "order_complete.html")

def place_order(request):
    return render(request, "place-order.html")

@login_required
@require_http_methods(["GET", "POST"])
def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    product_gallery = ImageGallery.objects.filter(product=product)
    
    driver_form = DriverForm(request.POST or None, request.FILES or None, prefix="driver")
    trailer_form = TrailerForm(request.POST or None, prefix="trailer")
    trailer_file_form = TrailerFileForm(request.POST or None, request.FILES or None, prefix="trailerfile")
    application_form = ApplicationForm(request.POST or None, prefix="application")

    if request.method == 'POST':
        dname = request.POST.get('dname')
        dpass = request.POST.get('dpassport')
        dletsence = request.POST.get('dletsence')
        dimg = request.FILES.get('dimg')
        url1 = f'static/images/{dname}.jpg'
        handle_upload(dimg, url1)
        crd = request.POST.get('crd')
        ctype = request.POST.get('ctype')
        cedangi = request.POST.get('cedangi')
        cmadename = request.POST.get('cmadename')
        ccefno = request.POST.get('ccefno')
        cimg = request.FILES.get('cimg')
        url2 = f'static/images/{crd}.jpg'
        handle_upload(cimg, url2)

        user_request = User_Request(dname=dname, dpass=dpass, dletsence=dletsence, url1=url1)
        user_request.save()
        user_request = UserRequest_Truck(crd=crd, ctype=ctype, cedangi=cedangi,cmadename=cmadename,ccefno=ccefno,url2=url2,dpass=dpass)
        user_request.save()

    context = {
        'single_product': product,
        'product_gallery': product_gallery,
        'driver_form': driver_form,
        'trailer_form': trailer_form,
        'trailer_file_form': trailer_file_form,
        'application_form': application_form
    }
    
    return render(request, 'product-detail.html', context)

def news(request):
    news_items = News.objects.all().order_by('-created_date')
    return render(request,'store/news.html',{'news_items': news_items})

def admin_user(request):
    news_items = Account.objects.all()
    return render(request,'admin/user.html',{'news_items': news_items})

def admin_category(request):
    news_items = Category.objects.all().order_by('-created_date')
    return render(request,'admin/category.html',{'news_items': news_items})

def admin_zar(request):
    news_items = Product.objects.all()
    if request.method == "POST":
        zname = request.POST.get('zname')
        desc = request.POST.get('ta_description')
        price = request.POST.get('price')
        zimg = request.FILES.get('image')
        ztype = request.POST.get('ztype')
        text_slug = translit(zname, 'ru', reversed=True)
        slug = text_slug.replace(" ", "")
        url = f'media/photos/products/{slug}.jpg'
        handle_upload(zimg, url)
        with sql.connect('db.sqlite3') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO 'store_app_product' (product_name, slug, description, price, images,stock,is_available,created_date,modified_date,category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (zname, slug, desc, price, url, 1, 0, formatted_datetime, 0, ztype))
            con.commit()
    return render(request,'admin/zar.html',{'news_items': news_items})

def admin_request(request):
    user_items = User_Request.objects.all()
    news_items = user_items
    truck = UserRequest_Truck.objects.all()
    return render(request,'admin/request.html',{'news_items': news_items,'context':truck})

def about(request):
    return render(request,'store/about.html')

def a(request):
    return render(request,'admin/a.html')

def search_result(request):
    return render(request, "search-result.html")

def store(request, category_slug = None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories)
        count=products.count()
        p=Paginator(products, 2)
        page = request.GET.get("page")
        paged_products = p.get_page(page)
    elif category_slug is None:
        products = Product.objects.filter(is_available = True)
        count=products.count()
        p=Paginator(products, 2)
        page = request.GET.get("page")
        paged_products = p.get_page(page)
    else:
        categories = Category.objects.all()
        products = Product.objects.filter(category = categories)
        count=products.count()
        p=Paginator(products, 2)
        page = request.GET.get("page")
        paged_products = p.get_page(page)
    context = {
        'products': paged_products,
        'categories': categories,
        'count': count
    }
    return render(request, "store/store.html", context) 
def home(request):
    categories = Category.objects.all()
    con  = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute("SELECT * FROM store_app_product")
    row = cur.fetchall()
    print(row)
    size = len(row)
    products = Product.objects.filter(is_available=True)
    context = {
        'categories': categories,
        'products': products,
        'size': size,
    }
    return render(request, "home.html", context)
def search(request):
    keyword = request.GET.get('keyword', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        min_price = float(min_price.replace(',', '.'))
    if max_price:
        max_price = float(max_price.replace(',', '.'))

    product_query = Q(product_name__icontains=keyword) | Q(description__icontains=keyword)

    if min_price is not None and max_price is not None:
        products = Product.objects.filter(product_query, price__gte=min_price, price__lte=max_price)
    else:
        products = Product.objects.filter(product_query)

    count = products.count()

    context = {
        'products': products,
        'count': count,
        'keyword': keyword,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'store/store.html', context)

def admin_index(request):
    application = Application.objects.all()
    ctx = {
        "applications": application
    }
    print(ctx)
    return render(request, 'admin/admin.html', ctx)


@require_POST
def update_applications(request):
    applications = Application.objects.all()
    for application in applications:
        checkbox_name = f'issuccess_{application.id}'
        application.issuccess = checkbox_name in request.POST
        application.save()
    return redirect('admin_index')