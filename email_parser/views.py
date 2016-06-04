from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def process_message(request):
	if request.method == 'POST':
         sender    = request.POST.get('sender')
         print('Sender = ', sender)
         recipient = request.POST.get('recipient')
         print('Recipient = ', recipient)
         subject   = request.POST.get('subject', '')
         print('Subject = ', subject)

         body_plain = request.POST.get('body-plain', '')
         print('body_plain = ', body_plain)
         body_without_quotes = request.POST.get('stripped-text', '')
         print('body_without_quotes = ', body_without_quotes)
         # note: other MIME headers are also posted here...

         # attachments:
         for key in request.FILES:
             file = request.FILES[key]
             print(file)
             # do something with the file

     # Returned text is ignored but HTTP status code matters:
     # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
	return HttpResponse('OK')