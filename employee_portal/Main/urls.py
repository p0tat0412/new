from django.urls import path
from .views import *


urlpatterns = [
    path('', home , name = 'home'),
    path('cpform/', cpform , name = 'cpform'),
    path('contact/<int:pk>/', contact , name = 'contact'),
    # urls.py
    path('coform/<int:company_id>/', coform, name='coform'),

    path('coform_update/<str:pk>/', coform_update , name = 'coform_update'),
    path('cpform_update/<str:pk>/', cpform_update , name = 'cpform_update'),
    path('company_delete/<str:pk>/', company_delete , name = 'company_delete'),
    path('contact_delete/<str:pk>/', contact_delete , name = 'contact_delete'),
    path('save-time', save_time, name='save_time'),
    path('login', login, name='login'),
    path('logout', logout_user, name='logout')
]