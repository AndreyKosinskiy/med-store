from django.urls import path
from .views import index, report
app_name = 'med_store'
urlpatterns = [
    path('', index,name='index'),
    path('report/', report,name='report'),
]