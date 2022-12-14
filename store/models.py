from django.db import models


# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount    = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # Circular Relationship: sometimes we can have multiple relationships between two models. So in soloution
    # for circular relationship is to name it something different or simply add a plus sign in related name.
    # Indeed Circular dependancy means two classes or table are dependent on each other at the same time.
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
   


class Product(models.Model):
    # to put our own primary key, we can write below code:
    # prim_key_field = models.CharField(max_length=10, primary_key=True)
    
    BRONZE_MEMBERSHIP='B'
    GOLD_MEMBERSHIP = 'G'
    DIAMOND_MEMBERSHIP = "D"

    MEMBERSHIP_SUBSCRIPTION=[
        (BRONZE_MEMBERSHIP,"Bronze"),
        (GOLD_MEMBERSHIP,"Gold"),
        (DIAMOND_MEMBERSHIP,"Diamond")
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places = 3)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # membership_choice = models.Choices(max_length=1,default=BRONZE_MEMBERSHIP)
    membership_choice = models.CharField(max_length=1, choices=MEMBERSHIP_SUBSCRIPTION, default=BRONZE_MEMBERSHIP)
    # one product can be once in a collection, but on the other hand one collection can have multiple 
    # products
    collection_of_products =  models.ForeignKey(Collection, verbose_name=("collection of multiple products"), on_delete=models.PROTECT)
    # also in another senario a collection can have one or zero featured_product
    #CASCADE.PROTECT means if we accedently deleted a collection all the products in that collection
    # should not be deleted.
    promotions = models.ManyToManyField(Promotion, verbose_name="Promotion for product",)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email      = models.EmailField(("email"), unique=True)
    phone      = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "F"
    placed_at   = models.DateTimeField(auto_now_add=True)

    PAYMENT_OPTION = [
        (PAYMENT_PENDING,"Pending"),
        (PAYMENT_COMPLETE,"Complete"),
        (PAYMENT_FAILED, "Failed")
    ]
    payment_status = models.CharField(max_length=1, choices=PAYMENT_OPTION,default=PAYMENT_PENDING)
    # One customer can have multiple one or multiple orders, So creation of foreignKey field for customer
    cutomer_order = models.ForeignKey(Customer, verbose_name=("order of customer"), on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name="Item of Order", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name="product as an Item", on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city   = models.CharField(max_length=255)
    # A OneToOneField is essentially the same as a ForeignKey,
    #  with the exception that it always carries a "unique" constraint with it and
    #  the reverse relation always returns the object pointed to (since there will only ever be one),
    #   rather than returning a list.
    customer = models.OneToOneField(Customer, verbose_name = "address of customer", on_delete=models.CASCADE, primary_key=True)
    # models.CASECADe means the associated address will also be deleted
    # models.SET_NULL means when we delete customer or the parent record the child field will be set to null
    # models.Default set with default value
    # models.PROTECT with this we can prevent the deletion or parent record can't be deleted


    # but if want that a customer can have multiple addresses wo we should create a ForeignKey field
    customer = models.ForeignKey(Customer, verbose_name=("addresses of customer"), on_delete=models.CASCADE)
    # we don't need primary_key=True because we want to have multiple addresses for the same customer.
    # in the theory of creation of relationship I should say, that like having multiple addresses for
    # just one customer we create a oneToOne or a foriegnKey field on the model that is in repeat or child for the 
    # parent like foreignKey of customer for address table


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=("cart of this item"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=("Product on this cart"), on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


