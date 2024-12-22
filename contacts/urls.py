from django.urls import path
from . import views

urlpatterns = [

    path('contact',views.contact, name='contact'),
    path('admin/contacts/export/excel/', views.admin_export_to_excel, name='admin_export_to_excel'),
    path('admin/contacts/export/pdf/', views.admin_export_to_pdf, name='admin_export_to_pdf'),
]
