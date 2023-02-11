from django.contrib import admin, messages
from . import models
# Register your models here.


admin.site.register(models.Collection)

# admin.site.register(models.Product)


class InventoryFilter(admin.SimpleListFilter): # Making a Custom Filter
    title = 'inventory'
    parameter_name = 'inventory'

    # To specify what items should appear in custome filter list
    def lookups(self, request, model_admin):
        
        # Now we return a tuple which very item of the tuple is an item of filtering
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


  

# for listing to objects to show we have to ways
# to learn more, search (django modelAdmin)
#1: by register decorator which is shorter way
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display =['title', 'unit_price','inventory_status']
    # but if we want to access the columns of other table which has relation with this table -
    # we should use display_select_related property. look at below example of list_display
    # list_display =['title', 'unit_price','inventory_status','collection']
    # but if want a specific column of collection table, we have to define a method for that like case1
    # list_display =['title', 'unit_price','inventory_status','collection_title']
    list_display =['title', 'unit_price','inventory_status','collection']
    list_editable=['unit_price']
    list_per_page=10
    list_select_related = ['collection']
    # adding filter to objects
    list_filter = ['collection','last_update',InventoryFilter] # adding Custom Filter
    # passing the name of custom action method
    actions = ['clear_inventory']

    #case1 definiation
     # Sorting the columns by with a new column(adding computed column)
    # e.g. we want to show a that if a the value of inventory of a product is less than 10 write(low) 
    @admin.display(ordering='inventory') # used for sorting
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
   #Creating Custom Actions
   # e.g. clearing the inventory of multiple products in one time
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} Products were successfully updated',
            messages.WARNING  # there different types of messages like: error, warning, success
        )
           



   


# #2. or if we don't use register decorator we can do this below method
# admin.site.register(models.Product, ProductAdmin)

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership_choice']
    list_editable=['membership_choice']
    ordering = ['first_name','last_name']
    list_per_page=10

    # adding search field 
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    

# Customizing Forms for adding and updating objects