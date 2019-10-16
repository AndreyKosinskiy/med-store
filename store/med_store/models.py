from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from .utils import get_info_from_excel, is_valid_or_list_error
# TODO:create manager for Document


class LogHandler(models.Model):
    #user = models.ForeignKey(User)
    action_object = models.CharField(max_length=120, null=True)
    action_method = models.CharField(max_length=120, null=True)
    action_result = models.CharField(max_length=120, null=True)
    action_date = models.DateTimeField(auto_now_add=True)


class ErorrHandler(models.Model):
    pass


class BaseClassObject(models.Model):
    name = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        LogHandler.objects.create(
            action_object=self.__class__,
            action_method="save",
            action_result=str(self),
        )
        super(BaseClassObject, self).save(*args, **kwargs) # Call the real save() method

    def __str__(self):
        return self.name


class Store(BaseClassObject):
    # TODO: add parent field mptt
    empty = models.BooleanField(default=False)


class DocumentManager(BaseClassObject):
    def analyser(self):
        return None


class Document(BaseClassObject):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=120, blank=True, null=True)
    attachment = models.FileField(upload_to='documents/%Y/%m/%d/user/', validators=[
                                  FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])])

    def get_table(self):
        return get_info_from_excel(self.attachment)['good_table']
    def get_doc_type(self):
        return get_info_from_excel(self.attachment)['doc_type']

    def save(self, *args, **kwargs):

        # Call the real save() method
        self.name = self.attachment.name
        self.doc_type = self.get_doc_type()
        super(Document, self).save(*args, **kwargs)
        table = self.get_table()
        for row in table:
                name, product_item_batch, qty, price = row[0].value, row[1].value, row[3].value, row[4].value
                obj_lot, created = Lot.objects.get_or_create(
                    product_item_batch=product_item_batch,
                    store=self.store,
                    name=name
                )
                obj_operation = Operation.objects.create(
                    name = obj_lot.name +' [ '+self.doc_type+' ] '+str(qty)+' штуки по цене '+str(price),
                    lot=obj_lot,
                    document=self,
                    operation_type=self.doc_type,
                    price=price,
                    qty=qty
                )


class Lot(BaseClassObject):
    product_item_batch = models.CharField(max_length=120)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def get_qty_all_operations(self):
        """
        Use it if Lot have one or more operations
        """
        result_list = []
        operation_list = Operation.objects.filter(lot=self)
        for operation in operation_list:
            if operation.operation_type == '-':
                result_list.append(-operation.qty)
            else:
                result_list.append(operation.qty)
        return sum(result_list)


class Operation(BaseClassObject):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=120)
    price = models.FloatField(null=False, blank=False)
    qty = models.IntegerField(null=False, blank=False)


class ProductItem(BaseClassObject):
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE)
    description = models.TextField(default=None)
