from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)

# lesson on caching
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects \
            .select_related('tags') \
                .filter(
                    content_type=content_type,
                    object_id = obj_id
                )
class TaggedItem(models.Model):

    objects = TaggedItemManager()
    # Which tag applied to which item
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


    # we could add a foreignKey of product class to taggetItem class for tagging the items, but it makes 
    # taggedItem dependent to just product class and if want to tag some other contents like videos or 
    # article, this taggedItem class won't work for them. Therefore we use the built-in contenttype class
    # so we comment the product foreign key
    # product = models.ForeignKey(Product)
    # so to use contentType class we have to identify the type and id of the object
    # using the type we can find the table and using the id we can find the record
    # for using the contenttpye we have to first import it
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,default=0)
    object_id = models.PositiveIntegerField(default=0.0)
    content_object = GenericForeignKey()





