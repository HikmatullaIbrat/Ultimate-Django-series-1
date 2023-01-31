from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from store.models import Collection , Promotion, Order
from django.db.models import Q
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from store.models import OrderItem, Customer
from django.db.models import DecimalField
 # we can import Count from aggregates or directly models
from django.db.models import Value, F, Func, Count, ExpressionWrapper
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from django.db import transaction

from django.db.models.functions import Concat
# Create your views here.


def say_salaam(request):
    # return HttpResponse('sanga yi!')
    # query_set = Product.objects.all()
    # filter will filterize the query_set by a condition
    # query_set.filter().filter()
    # query_set.count()
    # query_set.get(pk=1)
    # query_set(id=1)
    # query_set(any_fieldname=1)
    # query_set = Product.objects.get(pk=0) 
    # try:
    #     # product =  Product.objects.get(pk=0)
    #     # product =  Product.objects.first()
    #     product =  Product.objects.get(pk=0).first()
    #     print(product)
    # except ObjectDoesNotExist:
    #     pass
    product = Product.objects.filter(unit_price__gt=20)
    product = Product.objects.filter(unit_price__range=(20,30))
    product = Product.objects.filter(collection__id__range=(1,4))
    product = Product.objects.filter(title__icontains='coffee')
    collection = Collection.objects.filter(id__range=(1,5))
    product = Product.objects.filter(title__istartswith="coffee")
    product = Product.objects.filter(last_update__year=2021)
    # product = Product.objects.filter(last_update__dat=2021)
    product = Product.objects.filter(description__isnull=True)

    # Making Complex Queries
    # inventory <10 and price < 20
    product = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    product = Product.objects.filter(inventory__gt=20).filter(unit_price__lt=10)

    # Making Complex Queries using Q expressions
    product = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # return all products which inventory is less than 10 and unit_price is not less than 20
    product = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))

    # We can use F queries for assuring if one column value is equal to another one
    product = Product.objects.filter(inventory=F('unit_price'))
    product = Product.objects.filter(inventory=F('collection__id'))

    # sorting columns
    # 1. Ascending
    product = Product.objects.order_by('title')
    # 2. Descending
    product = Product.objects.order_by('-title')
    # multi layer sorting
    # this means to sort products with ascending order(cheapest) and if prices were equal 
    # so sort them in descending order of naming alphabet
    product = Product.objects.order_by('unit_price','-title')

    product = Product.objects.order_by('unit_price','-title') # completely opposite of the above operation
    product = Product.objects.filter(collection__id=1).order_by('unit_price')
    product = Product.objects.latest('unit_price')
    product = Product.objects.earliest('unit_price')

    # limiting objects
    product = Product.objects.all()[:5] # show first five objects
    product = Product.objects.all()[10:20]

    # limiting columns of objects
    product = Product.objects.values('id','description')
    # collection_title will return the values of collection table foriegn key for each table
    # values() method will return a dictionary list
    product = Product.objects.values('id','title','collection__title')

    #values_list() will return a tuple
    product = Product.objects.values_list('id','title','collection__title')

    # select product that have been ordered and sort them by their title
    product = Product.objects.filter( # distinct method removes the duplicate values
        id__in=OrderItem.objects.values('product_id').distinct()).order_by('title') 

    # for not selecting a column we use defer() method
    # Note: don't use the defered column in templated.
    product = Product.objects.defer('title')
    # To created a join between table (product,collection) we use select_related
    product = Product.objects.select_related('collection').all()
    # we can span other fields which has relation with collection
    # product = Product.objects.select_related('collection__someOtherField').all()

    # select_related used for one to one but prefetched_related used for many to many relationship
    product = Product.objects.select_related('collection').all()

    #for many to many field we use prefetch_related()
    product = Product.objects.prefetch_related('promotions').all()

    product = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # get last 5 order with their customer and items (including products)
    orders = Order.objects.select_related('customer').prefetch_related(
                            'orderitem_set__product').order_by('-placed_at')[:5]

    # Sometimes we need to summarize our objects so we use aggregate function
    result =  Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))

    # # we can do more operations with aggregate()
    # result =  Product.objects.filter(collection_id=1).aggregate(
    #             count=Count('id'), min_price=Min('unit_price'))

    # Annotating: in Django instead of the existed columns of models we can make new columns from the models
    # result = Product.objects.annotate(is_newColumn=Value(True))
    result = Product.objects.annotate(new_id=F('id') + 1)

    # Calling Database Functions with Func or with Django Database Functions
    result = Customer.objects.annotate(
        # CONCAT to show full name of customer first way using Func
        # F is referencing field of a model
        full_name = Func(F('first_name'), Value('   '), F('last_name'), function="CONCAT")
    )
    result = Customer.objects.annotate(
        # Second way using Concat method(should be imported)
        full_name = Concat('first_name', Value(" "), 'last_name')
    )

    # Grouping Data
    # e.g. List all the order of a customer
    result = Customer.objects.annotate(
        # in this query since Order model has a reverse relationship with Customer so we use that relation
        order_count=Count('order')
        )

    # Using ExpressionWrapper
    discounted_price = ExpressionWrapper(
        F('unit_price') * 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(
        discounted_price=discounted_price
    )

    # Querying Generic relationships
    # getting the tag for every Product
    # but every time we can't write this code so we make a manager from it and use that manager when needed
    content_type = ContentType.objects.get_for_model(Product)
    queryset=TaggedItem.objects \
        .select_related('tag') \
            .filter(
                content_type=content_type,
                object_id=1
            )

    # Lessons on Caching


                                                # Creating Objects
    # for creating objects we have two methods 1. save() 2. create()
    # 1. using save()
    # collection = Collection() 
    # adding a new value to collection category
    # collection.title = 'Video Game' 
    # we could use the below method of adding arguments, but it is not efficient more
    # collection = Collection(title='video games')

    # for adding a value of a relationship we use both below methods
    # collection.featured_product = Product(pk=1) # 1
    # collection.featured_product_id = 1          # 2
    # in the last we save the new inserted data with save()
    # collection.save()


    # 2. Using the create()
    # Collection.objects.create(title='History',featured_product_id='2')


                                                # Updating Object
    # 1. first way
    # collection = Collection.objects.get(pk=9)
    # collection.featured_product_id = 3
    # collection.save()


    # 2. second way using update()
    # Collection.objects.filter(pk=12).update(featured_product=3)
    # Collection.objects.filter(id__gt=5).update(featured_product=5)

                                                # Deleting Object
    # 1. first way
    # queryset = Collection.objects.get(pk=14)
    # queryset.delete()
 
    # 2. second way
    # Collection.objects.filter(id__gt=10).delete()


                                                #Transaction
    # Transaction should be imported
    # Transaction means to do two or multiple operation in once or don't anyone of them
    # e.g. inserting in order and order_item at same time
    # 1. first operation
    # in this case both of them are right
    with transaction.atomic():
        order =  Order()
        order.customer_id = 1
        order.save()

        # 2. Second Operation
        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    # one operation is not done, so second one will also be rolled back
    # with transaction.atomic():
    #     order =  Order()
    #     order.customer_id = 1
    #     order.save()

    #     # 2. Second Operation
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()
                                                        


    # print(product)
    # for prod in query_set:
    #     print(prod)

    # list(query_set)
    # query_set[0]
    # query_set[0:5]
    
    # return render(request, 'salam_alik.html',{'name':'Haroon',"products":product})
    # return render(request, 'salam_alik.html',{'name':'Haroon',"result":list(result)})
    return render(request, 'salam_alik.html',{'name':'Haroon',"queryset":list(queryset)})
    # return render(request, 'salam_alik.html',{query_set})
    # return render(request, 'salam_alik.html',{'name':'Haroon',"orders":orders})