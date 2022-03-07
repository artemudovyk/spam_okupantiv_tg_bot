from hashlib import new
import json
import logging
from django.views import View
from django.http import JsonResponse

from dtb.settings import DEBUG
from tgbot.dispatcher import process_telegram_event
from .models import Contact

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        print(request.body)
        if DEBUG:
            print('process event in debug')
            process_telegram_event(json.loads(request.body))
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)!
            # Read Procfile for details
            # You can run all of these services via docker-compose.yml
            print('process event')
            process_telegram_event.delay(json.loads(request.body))

        # TODO: there is a great trick to send action in webhook response
        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})


@csrf_exempt
@require_http_methods(["POST"])
def post_contact(request):
    data = json.loads(request.body)
    phone = data['phone']
    username = data['username']
    
    new_contact = Contact(phone_number=phone, username=username)
    new_contact.save()

    return JsonResponse({'success': f'Contact created: {new_contact.phone_number}, {new_contact.username}'})


@csrf_exempt
@require_http_methods(["POST"])
def post_contact_batch(request):
    data = json.loads(request.body)
    users = data['users']
    for user in users:
        phone = user['phone']
        username = user['username']
    
        new_contact = Contact(phone_number=phone, username=username)
        new_contact.save()

    return JsonResponse({'success': f'{len(users)} contacts created'})


@require_http_methods(["GET"])
def get_all_phone_numbers(request):
    all_contacts = Contact.objects.all()
    
    phone_numbers = [contact.phone_number for contact in all_contacts if contact.phone_number]
    
    return JsonResponse({
        "phone_numbers": phone_numbers,
    })