from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Collection)

# admin.site.register(models.Product)

# for listing to objects to show we have to ways
# to learn more, search (django modelAdmin)
#1: by register decorator which is shorter way
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =['title', 'unit_price','inventory_status']
    list_editable=['unit_price']
    list_per_page=10
     # Sorting the columns by with a new column(adding computed column)
    # e.g. we want to show a that if a the value of inventory of a product is less than 10 write(low) 
    @admin.display(ordering='inventory') # used for sorting
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
 

# #2. or if we don't use register decorator we can do this below method
# admin.site.register(models.Product, ProductAdmin)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership_choice']
    list_editable=['membership_choice']
    ordering = ['first_name','last_name']
    list_per_page=10

   