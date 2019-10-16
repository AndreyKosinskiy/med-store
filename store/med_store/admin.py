from django.contrib import admin
from .models import Store,Operation,Lot,ProductItem,Document,LogHandler

# Register your models here.
@admin.register(LogHandler)
class StoreAdmin(admin.ModelAdmin):
    model = LogHandler
    #list_display = ['title', 'author__name', ]

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    model = Store
    #list_display = ['title', 'author__name', ]

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    readonly_fields = ("name",'lot',"document","operation_type","qty","price")
    model = Operation
    #list_display = ['title', 'author__name', ]
class OperationInline(admin.TabularInline):
    model = Operation
    readonly_fields = ("name",'lot',"document","operation_type","qty","price")

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    model = Lot
    inlines = [
        OperationInline,
    ]


@admin.register(ProductItem)
class GoodAdmin(admin.ModelAdmin):
    model = ProductItem
    #list_display = ['title', 'author__name', ]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    model = Document
    #list_display = ['title', 'author__name', ]

