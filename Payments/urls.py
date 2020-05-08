from django.urls import path
from .views import initiate_payment, callback

urlpatterns = [
    path('sponsor/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    # path('return_pdf/', return_pdf, name='return_pdf')
]
