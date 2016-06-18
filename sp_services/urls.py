from django.conf.urls import url

urlpatterns = [
    url(r'bill', 'sp_services.views.get_bill'),
]