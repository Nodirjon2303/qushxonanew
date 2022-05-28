from django.shortcuts import render
from telegram import  Update
from telegram.ext import CallbackContext
import datetime
import pytz

def start(update:Update, context:CallbackContext):
    update.message.reply_text("Salom mening ismim Jarvin\nMen qushxonalarni avtomatlashtirish uchun tuzilgan botman\n"
                              "Savol va takliflar uchun @ruzimurodov_nodir")


def run_day_morning(context:CallbackContext):
    pass

def command_admin_key(update, context):
    update.message.reply_html("Ishladi")
    if update.effective_user.id == 881319779:
        context.job_queue.run_daily(run_day_morning,
                                    datetime.time(hour=8, minute=30, second=0, tzinfo=pytz.timezone('Asia/Tashkent')),
                                    days=(0, 1, 2, 3, 4, 5, 6))
