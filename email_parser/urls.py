from django.conf.urls import url

urlpatterns = [
    url(r'', 'email_parser.views.process_message'),
]