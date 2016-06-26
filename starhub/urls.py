from django.conf.urls import url

urlpatterns = [
    url(r'bill', 'starhub.views.get_bill'),
]