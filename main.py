from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.utils import exceptions
import asyncio
from pathlib import Path
from aiogram.types import ContentType, File, Message
import os

API_TOKEN = '6546656668:AAFjH_g2jwl09gVR3X1aHHAT1UiCm4z4zXU'


# Initialize bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать в Телеграм бота по созданию демотиваторов.\nДля начала отправьте мне фото и описание, а я сделаю демотиватор.")
@dp.message_handler(content_types=['any'])
async def handle_docs_photo(message):

    if message.content_type == "photo" or (message.reply_to_message and message.reply_to_message.content_type == "photo"):
        id = message.chat.id
        if message.reply_to_message: await message.reply_to_message.photo[-1].download(f'{id}.png')
        else: await message.photo[-1].download(f'{id}.png')

        fnt = ImageFont.truetype("arial.ttf", 80)

        img_list = 'preset.png'

        img = Image.open(img_list)
        usr_img = Image.open(f'{id}.png').convert("RGBA")

        usr_img = usr_img.resize((1050, 710))
        img.paste(usr_img, (118, 103),  usr_img)

        if message.caption: text = message.caption
        else: text = message.text if message.reply_to_message else ""
        if text == ".": text = ""  


        fnt = ImageFont.truetype("arial.ttf", 80)
        width = fnt.getsize(text)[0]
        i = 0
        while width > 1050 or i > 78:
            fnt = ImageFont.truetype("arial.ttf", 80 - i)
            width = fnt.getsize(text)[0]
            i += 1

        d = ImageDraw.Draw(img)
        width = fnt.getsize(text)[0]

        d.text((640 - (width / 2), 858), text, font=fnt, fill=(255, 255, 255, 255))

        img.save("1" + f'{id}.png')

        photo = open("1" + f'{id}.png', 'rb')
        await message.answer_photo(photo)
        photo.close()
        os.remove("1" + f'{id}.png')
        os.remove(f'{id}.png')



if __name__ == '__main__':
    # start bot
    executor.start_polling(dp, skip_updates=True)