import datetime
from random import randint

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from . import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User, Contact
from .keyboards import make_keyboard_for_contact_command

def command_contact(update: Update, context: CallbackContext) -> None:
    # u, created = User.get_user_and_created(update, context)

    # if created:
    #     text = static_text.start_created.format(first_name=u.first_name)
    # else:
    #     text = static_text.start_not_created.format(first_name=u.first_name)

    # update.me/ssage.reply_text(text=text,
    #                           reply_markup=make_keyboard_for_start_command())
    
    user = User.get_user(update, context)
    
    try:
        contact = _get_new_contact(user)
    except Exception as e:
        print(user)
    
    update.message.reply_text(text=f'Давай почнемо з:\n{contact.phone_number}\n@{contact.username}', reply_markup=make_keyboard_for_contact_command())
    
    
def contact_success(update: Update, context: CallbackContext) -> None:
    # """Parses the CallbackQuery and updates the message text."""
    try:
        # Get user
        user_id = extract_user_data_from_update(update)['user_id']
        user = User.objects.get(user_id=user_id)
        
        # Add successful repeat to the current contact
        phone_number = update['callback_query']['message']['text'].split('\n')[1].split(': ')[-1]
        contact = Contact.objects.get(phone_number=phone_number)
        contact.add_repeat()
        user.add_contact_to_processed(contact)
        user.increment_success_num()
        
        # Answer to query and show user notification
        query = update.callback_query
        query.answer('Успіх!')
        
        # Edit message with new text
        text_for_previous_message = f"✅Успіх!\n{_get_text_for_old_contact(contact)}"
        query.edit_message_text(text=text_for_previous_message)
        
        # Get new contact
        new_contact = _get_new_contact(user)
        
        # Send new message
        # TODO: check if there's no contact for user to process
        # if not new_contact:
        #     update.callback_query.message.reply_text(text='Контактів для тебе більше немає. Дякуємо, що ти долучився до ініціативи!')
        new_text = _get_text_for_new_contact(new_contact, user)
        update.callback_query.message.reply_text(text=new_text, reply_markup=make_keyboard_for_contact_command())
    except Exception as e:
        print(e)

    
def contact_failed(update: Update, context: CallbackContext) -> None:
    try:
        # Get user
        user_id = extract_user_data_from_update(update)['user_id']
        user = User.objects.get(user_id=user_id)
        
        # Add successful repeat to the current contact
        phone_number = update['callback_query']['message']['text'].split('\n')[1].split(': ')[-1]
        contact = Contact.objects.get(phone_number=phone_number)
        contact.add_failed_repeat()
        user.add_contact_to_processed(contact)
        
        # Answer to query and show user notification
        query = update.callback_query
        query.answer("Не змогли зв'язатися")
               
        # Edit message with new text
        text_for_previous_message = f"❌Не змогли зв'язатися\n{_get_text_for_old_contact(contact)}"
        query.edit_message_text(text=text_for_previous_message)
        
        # Get new contact
        new_contact = _get_new_contact(user)
        
        # Send new message
        new_text = _get_text_for_new_contact(new_contact, user)
        update.callback_query.message.reply_text(text=new_text, reply_markup=make_keyboard_for_contact_command())
    except Exception as e:
        print(e)


def contact_skip(update: Update, context: CallbackContext) -> None:
    try:
        # Get user
        user_id = extract_user_data_from_update(update)['user_id']
        user = User.objects.get(user_id=user_id)
        
        # Add successful repeat to the current contact
        phone_number = update['callback_query']['message']['text'].split('\n')[1].split(': ')[-1]
        
        username = update['callback_query']['message']['text'].split('\n')[2].split(': ')[-1]
        if 'Логін в Telegram' not in username:
            username = ''
        
        contact = Contact.objects.get(phone_number=phone_number)
        contact.add_failed_repeat()
        user.add_contact_to_processed(contact)
        
        # Answer to query and show user notification
        query = update.callback_query
        query.answer('Пропущено')
        
        # Edit message with new text
        text_for_previous_message = f"➡️Пропустили\n{_get_text_for_old_contact(contact)}"
        query.edit_message_text(text=text_for_previous_message)
        
        # Get new contact
        new_contact = _get_new_contact(user)
        
        # Send new message
        new_text = _get_text_for_new_contact(new_contact, user)
        update.callback_query.message.reply_text(text=new_text, reply_markup=make_keyboard_for_contact_command())
    except Exception as e:
        print(e)
    
    
def _get_new_contact(user: User):
    try:
        user_processed_contacts_numbers = [contact.phone_number for contact in user.contacts_processed.all()]
        contact = Contact.objects.exclude(phone_number__in=user_processed_contacts_numbers).first()
        if not contact:
            return None
        return contact
    except Exception as e:
        print(e) 
    
    
def _get_text_for_new_contact(contact, user):
    if contact.username:
        return f"Супер! Ти вже опрацював(ла) {len(user.contacts_processed.all())} контактів, з яких {user.success_num} - успішно. Давай ще один:\nТелефон: {contact.phone_number}\nЛогін в Telegram: {contact.username}\n\nСпробуй знайти його в Telegram (телефон або логін), або в Viber/Whatsapp по номеру телефона."
    else:
        return f"Супер! Ти вже опрацював(ла) {len(user.contacts_processed.all())} контактів, з яких {user.success_num} - успішно. Давай ще один:\nТелефон: {contact.phone_number}\n\nСпробуй знайти його в Telegram (телефон) або в Viber/Whatsapp по номеру телефона."
    

def _get_text_for_old_contact(contact):
    if contact.username:
        return f"Телефон: {contact.phone_number}\nЛогін в Telegram: {contact.username}"
    else:
        return f"Телефон: {contact.phone_number}"
    