
import telebot
import logging
import application.game.main_game as m
from telebot import types 
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot




from django.conf import settings


CHAT_ID = [-1002220173477]
logger = logging.getLogger(__name__)

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

player_1_score = 0
player_2_score = 0
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет это бот реализующий игру "ОЧКО".\nВаша задача набрать меньше 24 очков.\nНажмите начать для начала игры '
    markup = types.ReplyKeyboardMarkup()
    button_start = types.KeyboardButton("НАЧАТЬ")
    markup.add(button_start)
    await bot.send_message(message.chat.id, text = text,reply_markup=markup)

@bot.message_handler(content_types=['text'])
async def unfo(message):
    if message.text == 'НАЧАТЬ':
        markup = types.ReplyKeyboardMarkup()
        button_to_take = types.KeyboardButton("ВЗЯТЬ")
        button_to_leave = types.KeyboardButton("ОСТАВИТЬ")
        markup.add(button_to_take,button_to_leave)
        await bot.send_message(message.chat.id, f'Выберите "ВЗЯТЬ", что-бы взять карту или "ОСТАВИТЬ"', reply_markup=markup)
    elif message.text == 'ВЗЯТЬ':
        global player_1_score
        global player_2_score
        m.main_games()
        markup = types.ReplyKeyboardMarkup()
        button_to_take = types.KeyboardButton("ВЗЯТЬ")
        button_to_leave = types.KeyboardButton("ОСТАВИТЬ")
        markup.add(button_to_take,button_to_leave)
        await bot.send_message(message.chat.id,f'Ваш результат:{m.player_1_score}', reply_markup=markup)
        if m.player_1_score >= 24:
            markup = types.ReplyKeyboardMarkup()
            button_start = types.KeyboardButton("НАЧАТЬ")
            markup.add(button_start)
            if m.player_1_score and m.player_2_score >= 24:
                markup = types.ReplyKeyboardMarkup()
                button_start = types.KeyboardButton("НАЧАТЬ")
                markup.add(button_start)
                await bot.send_message(message.chat.id, f'Игра окончена 😉НИЧЬЁЙ😉\nВы набрали 24 или больше очков,а ваш соперник:{m.player_2_score}',  reply_markup=markup)
                m.player_1_score = 0
                m.player_2_score = 0
            elif m.player_2_score < 24:
                markup = types.ReplyKeyboardMarkup()
                button_start = types.KeyboardButton("НАЧАТЬ")
                markup.add(button_start)
                await bot.send_message(message.chat.id, f'Игра окончена 😢ПОБЕДОЙ СОПЕРНИКА😢\nВы набрали 24 или больше очков,а ваш соперник:{m.player_2_score}',  reply_markup=markup)
                m.player_1_score = 0
                m.player_2_score = 0
    elif message.text == 'ОСТАВИТЬ':
        markup = types.ReplyKeyboardMarkup()
        button_start = types.KeyboardButton("НАЧАТЬ")
        markup.add(button_start)
        if m.player_1_score < m.player_2_score:
            markup = types.ReplyKeyboardMarkup()
            button_start = types.KeyboardButton("НАЧАТЬ")
            markup.add(button_start)
            await bot.send_message(message.chat.id, f'Игра окончена 😢ПОБЕДОЙ СОПЕРНИКА😢\nВы набрали меньше очков чем у соперника\nЕго результат:{m.player_2_score}',  reply_markup=markup)
            m.player_1_score = 0
            m.player_2_score = 0
        elif m.player_1_score > m.player_2_score:
            markup = types.ReplyKeyboardMarkup()
            button_start = types.KeyboardButton("НАЧАТЬ")
            markup.add(button_start)
            await bot.send_message(message.chat.id, f'Игра окончена вы ❤️‍🔥ПОБЕДИЛИ❤️‍🔥\nВы набрали больше очков чем у соперника\nЕго результат:{m.player_2_score}',  reply_markup=markup)
            m.player_1_score = 0
            m.player_2_score = 0
        elif m.player_1_score == m.player_2_score:
            markup = types.ReplyKeyboardMarkup()
            button_start = types.KeyboardButton("НАЧАТЬ")
            markup.add(button_start)
            await bot.send_message(message.chat.id, f'Игра окончена 😉НИЧЬЁЙ😉\nВы набрали одинаковое количество очков\nЕго результат:{m.player_2_score}',  reply_markup=markup)
            m.player_1_score = 0
            m.player_2_score = 0

    else:
        text = 'Нажмите "НАЧАТЬ" для начала игры'
        await bot.send_message(message.chat.id, text = text)
        





@bot.chat_member_handler() 
async def chat_member_handler_bot(message: Message):
    if message.chat.id is not CHAT_ID:
        return None
    status = message.difference.get('status')
    invite_link = message.invite_link
    full_name = message.from_user.full_name
    username = message.from_user.username
    id = message.from_user.id
    invite_link_name = ''
    invite_link_url = ''
    try:
        invite_link_name = getattr(invite_link, 'name')
        invite_link_url = getattr(invite_link, 'invite_link')
    except AttributeError as err:
        logger.info(f'Не получил пригласительную ссылку: {err}')
    status_subscriber = status[1]
    if status_subscriber == 'member':
        status_text = '❤️‍🔥 Подписался'
    elif status_subscriber == 'left':
        status_text = '💔 Отписался'
    else:
        status_text = '😐 Неизвестно'

    text_message = (f'Статус: {status_text}\n'
                    f'Имя: {full_name}\n'
                    f'ID: {id}')
    if username:
        text_message += f'\n<b>Никинейм</b>: @{username}'
    if invite_link_name:
        text_message += f'\nИмя ссылки: {invite_link_name}'
    if invite_link_url:
        text_message += f'\n<b>URL</b>: {invite_link_url}'
    
    await bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN, text=text_message)



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker'])
async def default_command(message):
    await bot.send_message(message.chat.id, "I don't understand you. Please write /start or /help ")