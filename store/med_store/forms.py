from django import forms
from .models import Document
from .utils import get_info_from_excel, is_valid_or_list_error,build_book
from django.forms.utils import ErrorList
from .models import Lot, Operation, Store, Report
from django.contrib.admin import widgets


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        else:
            return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger col-md-12 text-center">%s</div>' % e for e in self])

class DocumentForm(forms.ModelForm):

    class Meta:
        model=Document
        fields=('attachment', 'store')
        widgets={
            'attachment': forms.FileInput(attrs={'class': 'form-control-file'}),
            'store': forms.Select(attrs={'class': 'custom-select'}),
        }

    def __init__(self, *args, **kwargs):
        # TODO: I`m not shure what it is not Fail
        kwargs_new={'error_class': DivErrorList}
        kwargs_new.update(kwargs)
        super(DocumentForm, self).__init__(*args, **kwargs_new)

    def clean(self):
        cleaned_data=super().clean()
        input_document=cleaned_data.get("attachment")
        # return table witout header
        excel_book=get_info_from_excel(input_document)
        analyzer_result=is_valid_or_list_error(excel_book)
        if analyzer_result != True:
            for msg, result in analyzer_result.items():
                if result == False:
                    self.add_error("attachment", msg+"Fail")
        else:
            store=Store.objects.get(name=cleaned_data.get("store"))
            for row in excel_book['good_table']:
                name, product_item_batch, qty, price=row[0].value, row[1].value, row[3].value, row[4].value
                # TODO: Can be in one file two or more LOT?
                is_exists_lot=Lot.objects.filter(
                    product_item_batch=product_item_batch,
                    store=store,
                    name=name
                ).exists()
                if excel_book['doc_type'] == '-':
                    if is_exists_lot:
                        obj_lot=Lot.objects.get(
                            product_item_batch=product_item_batch,
                            store=store,
                            name=name
                        )

                        exists_qty=obj_lot.get_qty_all_operations()
                        if exists_qty < qty:
                            self.add_error(
                                "attachment", f"New qty in attachment biggest then qty of product you have now lot {product_item_batch}: you want substruct {qty} but {exists_qty} you have now.")
                    elif not is_exists_lot:
                        self.add_error(
                            "attachment", f"You want substruct {qty} in {product_item_batch} lot, which not exists.")

class ReportForm(forms.Form):
    all_store = Store.objects.all()
    list_store_select = []
    for store in all_store:
        list_store_select.append((store.id, store.name))

    CHOICES = (('Option 1', 'Option 1'), ('Option 2', 'Option 2'),)

    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    store = forms.ChoiceField(
        choices=list_store_select, 
        widget=forms.Select(attrs={'class': 'custom-select'})
    )
    def save(self):
        print(self.cleaned_data["store"])
        print(self.cleaned_data["start_date"])
        print(self.cleaned_data["end_date"])
        store = Store.objects.get(id=self.cleaned_data["store"])
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        Report.objects.create(
            store = store,
            start_date = self.cleaned_data["start_date"],
            end_date = self.cleaned_data["end_date"]
        )
        lots_in_store = Lot.objects.filter(store = store)
        report_table = []
        for lot in lots_in_store:
            report_table.append([lot.name,lot.product_item_batch,lot.get_qty_all_operations(start_date,end_date)])
        print(report_table)
        response = build_book([start_date,end_date],report_table)
        print("Ау блять!")
        return response
        