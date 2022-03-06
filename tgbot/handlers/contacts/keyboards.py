from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def make_keyboard_for_contact_command() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton('✅Готово', callback_data='success')],
        [InlineKeyboardButton('❌Не змогли зв\'язатися', callback_data='failed')],
        [InlineKeyboardButton('➡️Пропустити', callback_data='skip')],
    ]

    return InlineKeyboardMarkup(buttons)
