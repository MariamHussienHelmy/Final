from django.urls import path
from pdf_generator.views import generate_pdf

urlpatterns = [
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('generate_pdf/<str:kit_code>/', generate_pdf, name='generate_pdf_with_kit_code'),
]
