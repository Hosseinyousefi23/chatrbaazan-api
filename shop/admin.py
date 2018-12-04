from django.contrib import admin

# Register your models here.
from shop.models import City, Banner, Product, Category, Company, ProductLabel, Discount, ProductGallery

admin.site.register(City)
admin.site.register(Banner)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(ProductLabel)
admin.site.register(Discount)
admin.site.register(ProductGallery)

