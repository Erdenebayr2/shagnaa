from django.db import models
from django.urls import reverse
from accounts.models import Account
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    def __str__ (self):
        return self.category_name
    def get_url(self):
        return reverse('store', args=[self.slug])
class Product(models.Model):

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.product_name
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
class ImageGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)
    def __str__(self):
        return self.product.product_name
    
    
class Trailer(models.Model):
    register = models.CharField(max_length=255)
    vehicletype = models.CharField(max_length=255)
    edangi = models.CharField(max_length = 255)
    trademark_or_manufacturer = models.CharField(max_length=255)
    certificate_number = models.CharField(max_length=255)
    def __str__(self):
        return self.register
    
class TrailerFile(models.Model):
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)
    file = models.FileField(upload_to='store/files')
    def __str__(self):
        return self.trailer.register

class Application(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    driver = models.ForeignKey(Account, on_delete=models.CASCADE)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)
    issuccess = models.BooleanField()
    def __str__(self):
        return self.driver.user.first_name


class News(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.title
    
class User_Request(models.Model):
    dname = models.CharField(max_length=100)
    dpass = models.CharField(max_length=100)
    dletsence = models.CharField(max_length=100)
    url1 = models.CharField(max_length=200)
    def __str__ (self):
        return self.dname

class UserRequest_Truck(models.Model):
    crd = models.CharField(max_length=100)
    ctype = models.CharField(max_length=100)
    cedangi = models.CharField(max_length=100)
    cmadename = models.CharField(max_length=100)
    ccefno = models.CharField(max_length=100)
    url2 = models.CharField(max_length=200)
    dpass = models.CharField(max_length=100)
    def __str__ (self):
        return self.crd
