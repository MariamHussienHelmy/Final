from django.urls import path
from pdf_generator.views import generate_report

urlpatterns = [
    path('generate_report/', generate_report, name='generate_report'),
    path('generate_report/<str:kit_code>/', generate_report, name='generate_report_with_kit_code'),
]
