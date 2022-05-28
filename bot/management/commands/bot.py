from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from django.conf import settings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler

from bot.views import *


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=None,
            read_timeout=None
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )
        conv_hand = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text, start)
            ],
            states={


            },
            fallbacks=[
                CommandHandler('start', start)
            ]

        )
        updater.dispatcher.add_handler(conv_hand)

        updater.start_polling()
        updater.idle()
