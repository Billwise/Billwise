from django.conf.urls import url

urlpatterns = [
    url(r'bill', 'singtel.views.get_bill'),
]