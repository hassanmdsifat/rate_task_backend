from django.urls import path

from api.views.rate_views import RateView

urlpatterns = [
    path('rates/', RateView.as_view(), name='get-rates'),
]