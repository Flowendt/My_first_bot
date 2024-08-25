import asyncio
import logging

from telebot import util
from django.conf import settings
from application.main_bot import bot
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        try:
            asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL, allowed_updates=util.update_types))
        except Exception as err:
            logger.error(f'Ошибка:{err}')
