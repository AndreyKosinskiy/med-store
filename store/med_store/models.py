from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from django.db import connection
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from .utils import get_info_from_excel, is_valid_or_list_error, build_book
import datetime

# TODO:create manager for Document


class LogHandler(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    action_object = models.CharField(max_length=120, null=True)
    action_method = models.CharField(max_length=120, null=True)
    action_result = models.CharField(max_length=120, null=True)
    action_date = models.DateTimeField(auto_now_add=True)


class ErorrHandler(models.Model):
    pass


class BaseClassObject(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=120)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseClassObject, self).save(
            *args, **kwargs)  # Call the real save() method
        # LogHandler.objects.create(
        #     user = self.user,
        #     action_object=self.__class__,
        #     action_method="save",
        #     action_result=str(self),
        # )

    def __str__(self):
        return self.name


class Store(BaseClassObject):
    # TODO: add parent field mptt
    empty = models.BooleanField(default=False)


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
        print("Model: ", self.user)
        user = self.user
        self.name = self.attachment.name
        self.doc_type = self.operation_btn
        super(Document, self).save(*args, **kwargs)
        
        store = self.store
        table = self.get_table()
        obj_operations = []
        lot_qs_by_store = Lot.objects.all().select_related("store").filter(store=store)
        for row in table:
            name, product_item_batch, qty, price = row[2].value, row[1].value, row[5].value, row[7].value
            if None in (name, product_item_batch, qty, price):
                continue
            if isinstance(qty, str,):
                qty = float(qty.replace(',', '.'))
            elif isinstance(price, str,):
                price = float(price.replace(',', '.'))
            lot_qs_by_instance = lot_qs_by_store.filter(
                product_item_batch=product_item_batch, 
                name=name
            )
            a = datetime.datetime.now()
            obj_lot,created =lot_qs_by_instance.get_or_create(
                user=user,
                store = store,
                product_item_batch=product_item_batch,
                name=name
            )
            print("for row procces in isinstance: ", datetime.datetime.now()-a)
            obj_operations.append(Operation(
                user=user,
                name=obj_lot.name +
                ' [ '+self.doc_type+' ] ' +
                str(qty)+' штуки по цене '+str(price),
                lot=obj_lot,
                document=self,
                operation_type=self.doc_type,
                price=price,
                qty=qty
            ))
        Operation.objects.bulk_create(obj_operations)



class Lot(BaseClassObject):
    product_item_batch = models.CharField(max_length=120)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def get_qty_all_operations(self, start_date=None, end_date=None):
        """
        Use it if Lot have one or more operations
        """
        result_list = []
        operation_list = None

        if start_date == None and end_date == None:
            #print("start_date == None and end_date == None")
            operation_list = Operation.objects.filter(lot=self)
        elif start_date == None:
           # print("start_date == None")
            operation_list = Operation.objects.filter(
                lot=self, created_date__date__lte=end_date)
        elif end_date == None:
            #print("end_date == None")
            operation_list = Operation.objects.filter(
                lot=self, created_date__date__gte=start_date)
        else:
            operation_list = Operation.objects.filter(
                lot=self, created_date__range=(start_date, end_date))
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


class Report (BaseClassObject):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=True, blank=True, null=True)
    end_date = models.DateTimeField(editable=True, blank=True, null=True)
