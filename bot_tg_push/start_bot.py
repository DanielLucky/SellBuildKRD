import asyncio
import requests
import datetime as dt

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor

from connect_db import parse_data
from config import TOKEN

CHANNEL_ID = -1001460850279

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def main():
    while True:
        q_dict = parse_data()
        # print('q_dict', q_dict)
        if q_dict != {}:
            for target in q_dict:
                # print(q_dict[target])
                text_massage = f"<b>{q_dict[target]['nameSell']}</b>\n" \
                               f"<b>Адрес:</b> {q_dict[target]['address']}\n" \
                               f"<b>Ремонт:</b> {q_dict[target]['furnish']}\n" \
                               f"<b>Описание:</b> {q_dict[target]['specifications']}\n" \
                               f"<b>Цена:</b> {q_dict[target]['price']}\n" \
                               f"<b>Телефон:</b> {q_dict[target]['telephone']}\n"

                if q_dict[target]['headerImage'] == 'https://lucky-spb.online/':
                    image = 'https://lucky-spb.online/media/images/KVARTIRA.png'
                else:
                    if requests.get(q_dict[target]['headerImage']).status_code != 404:
                        image = q_dict[target]['headerImage']
                    else:
                        image = 'https://lucky-spb.online/media/images/KVARTIRA.png'

                media = [InputMediaPhoto(image, text_massage, parse_mode=types.ParseMode.HTML)]
                for image in q_dict[target]['image_list']:
                    if requests.get(image).status_code != 404:
                        media.append(image)
                await bot.send_media_group(CHANNEL_ID, media)
        await asyncio.sleep(15)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp)
