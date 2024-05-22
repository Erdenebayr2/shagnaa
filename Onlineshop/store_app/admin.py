from django.contrib import admin
from .models import Category, Product, ImageGallery, Trailer, TrailerFile, Application,News, User_Request, UserRequest_Truck
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
admin.site.register(Category, CategoryAdmin)
class ImageGalleryTabular(admin.TabularInline):
    model = ImageGallery
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ImageGalleryTabular]
admin.site.register(Product, ProductAdmin)

admin.site.register(Trailer)
admin.site.register(Application)
admin.site.register(News)
admin.site.register(User_Request)
admin.site.register(UserRequest_Truck)