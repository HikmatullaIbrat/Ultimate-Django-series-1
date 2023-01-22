from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
from store.models import Collection , Promotion
from django.db.models import Q
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from store.models import OrderItem
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

    # print(product)
    # for prod in query_set:
    #     print(prod)

    # list(query_set)
    # query_set[0]
    # query_set[0:5]
    
    return render(request, 'salam_alik.html',{'name':'Haroon',"products":product})
    # return render(request, 'salam_alik.html',{query_set})