from django.shortcuts import render

# Create your views here.
def process_message(request):
	return render(request, 'message_received.html')