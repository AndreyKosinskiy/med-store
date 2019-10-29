from django import forms
from django.forms.utils import ErrorList
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

import datetime
from datetime import date

from .models import Lot, Operation, Store, Report, Document
from .utils import get_info_from_excel, is_valid_or_list_error,build_book

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='Optional.', widget = forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=30, widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=30,  widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget = forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class LogInForm(forms.Form):
    username = forms.CharField(max_length=30, required=False, help_text='Optional.', widget = forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=30, widget = forms.PasswordInput(attrs={'class': 'form-control'}))

class ErrorList(ErrorList):
    def __str__(self):
        return self.as_table()

    def as_table(self):
        if not self:
            return ''
        else:
            return '<table class="table table-sm"><thead><tr><th scope="col">#</th><th scope="col">Назва</th><th scope="col">Партия</th><th scope="col">Нестача, од</th></tr></thead></tbody>%s</tbody></table>' % ''.join([f'<tr><th scope="row">{idx+1}</th><td>{error_list.split("|")[0]}</td><td>{error_list.split("|")[1]}</td><td>{error_list.split("|")[2]}</td></tr>' for idx,error_list in enumerate(self)])

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
        self.operation_btn = kwargs.pop('operation_btn')
        kwargs_new={'error_class': ErrorList}
        kwargs_new.update(kwargs)
        super(DocumentForm, self).__init__(*args, **kwargs_new)


    def clean(self):
        cleaned_data=super().clean()
        input_document=cleaned_data.get("attachment")
        operation_btn = self.operation_btn
        # # return table witout header
        excel_book=get_info_from_excel(input_document)
        analyzer_result=is_valid_or_list_error(excel_book)
        if analyzer_result != True:
            for msg, result in analyzer_result.items():
                if result == False:
                    self.add_error("attachment", msg+"Fail")
        else:
            store= Store.objects.get(name=cleaned_data.get("store"))
            
            lots_qs = Lot.objects.all().select_related("store").filter(store=store)
            for row in excel_book['good_table']:
                #name, product_item_batch, qty, price=row[0].value, row[1].value, row[3].value, row[4].value
                name, product_item_batch, qty, price = row[2].value, row[1].value, row[5].value, row[7].value
                if None in (name, product_item_batch, qty, price):
                    continue
                # TODO: Can be in one file two or more LOT?
                if operation_btn == '-':
                    
                    obj_lot = lots_qs.filter(
                        product_item_batch=product_item_batch
                    )
                    
                    
                    is_exists_lot = obj_lot.exists()
                    if is_exists_lot:
                        obj_lot = obj_lot.first()
                        c = datetime.datetime.now()
                        exists_qty=obj_lot.get_qty_all_operations()
                        
                        if exists_qty < qty:
                            deficit_count = qty-exists_qty
                            self.add_error("attachment",  f'{name}|{product_item_batch}|{deficit_count}')
                    elif not is_exists_lot:
                        deficit_count = "Товар відсутній"
                        self.add_error("attachment", f'{name}|{product_item_batch}|{deficit_count}')
        
        

class ReportForm(forms.Form):
    CHOICES = (('Option 1', 'Option 1'), ('Option 2', 'Option 2'),)

    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }),
        required = False
    )
    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        }),
        required = False
    )
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'custom-select'}
        )
    )

    def save(self):
        store = self.cleaned_data["store"]#Store.objects.get(id=self.cleaned_data["store"])
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        Report.objects.create(
            store = store,
            start_date = start_date,
            end_date = end_date
        )
        lots_in_store = Lot.objects.filter(store = store)
        report_table = []
        for lot in lots_in_store:
            report_table.append([lot.name,lot.product_item_batch,lot.get_qty_all_operations(start_date,end_date)])
        print(report_table)
        response = build_book([start_date,end_date],report_table)
        if start_date:
            start_date = start_date.date().strftime("%d/%m/%Y")
        if end_date:
            end_date = end_date.date().strftime("%d/%m/%Y")
        #return response
        return start_date, end_date, report_table