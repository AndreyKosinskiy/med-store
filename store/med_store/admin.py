from django.contrib import admin
from .models import Store,Operation,Lot,Good,Document

# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    model = Store
    #list_display = ['title', 'author__name', ]

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    model = Operation
    #list_display = ['title', 'author__name', ]
class OperationInline(admin.TabularInline):
    model = Operation
    readonly_fields = ["name",'lot',"document","operation_type","qty"]

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    model = Lot
    inlines = [
        OperationInline,
    ]


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    model = Good
    #list_display = ['title', 'author__name', ]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    model = Document
    #list_display = ['title', 'author__name', ]

