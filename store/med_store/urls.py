from django.urls import path
from .views import index, report, signup , logout_view ,login_view
app_name = 'med_store'
urlpatterns = [
    path('', index,name='index'),
    path('signup/', signup,name='signup'),
    path('logout/', logout_view, name='logout'),
    path('report/', report,name='report'),
    path('login/' , login_view , name="login")
]