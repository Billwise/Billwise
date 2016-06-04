from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

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
         send_simple_message(sender, "Re: " + subject)

     # Returned text is ignored but HTTP status code matters:
     # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
         return HttpResponse('OK')

def send_simple_message(recipient_email_id, subject):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxaeedb52bbc344d3db562ce0ddc5fb584.mailgun.org/messages",
        auth=("api", "key-ae6af4f4c6a04a3f48fa506094189246"),
        # data={"from": "Billwise postmaster@sandboxaeedb52bbc344d3db562ce0ddc5fb584.mailgun.org",
        data={"from": "Billwise super-smart-ai@api.billwise.co",      
              "to": [recipient_email_id],
              "subject": subject,
              "text": "Hey, thanks for sending us your bill. We will parse it and add it to our knowledge base. Our bots are already at work using the new information to make your bill-paying existence better and more useful."})

@csrf_exempt
def process_hook_from_context(request):
	return HttpResponse('OK')

def process_receipt_message(request):
	print("Receipt callback called")
	return HttpResponse('OK')