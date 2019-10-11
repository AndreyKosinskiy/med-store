from django.db import models
#TODO:create manager for Document 


class LogHandler(models.Model):
    pass


class ErorrHandler(models.Model):
    pass


class BaseClassObject(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        abstract = True

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
    doc_type = models.CharField(max_length = 120)
    attachment = models.FileField(upload_to='Store/%Y/%m/%d/user/')

    objects = DocumentManager()
class Lot(BaseClassObject):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

class Operation(BaseClassObject):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length = 120)
    qty = models.IntegerField()

class Good(BaseClassObject):
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE)
    description = models.TextField(default=None)
