from django.conf.urls import url

urlpatterns = [
	url(r'context-message', 'email_parser.views.process_hook_from_context'),
	url(r'context-message/receipt', 'email_parser.views.process_receipt_message'),
    url(r'', 'email_parser.views.process_message'),
]