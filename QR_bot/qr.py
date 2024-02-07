import qrcode
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from PIL import Image


BOT_TOKEN = '6205323230:AAGhKSx77wTFQO4RqTw5YUgPBK_xqvEQeo4'

bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
dp = Dispatcher(bot) 
qr_code_text = ""

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    kb = [
       [
            types.KeyboardButton(text="QR-code")
       ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    # Приветственное сообщение при команде /start
    await message.reply('Привет👋\nЯ могу делать QR коды.', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "QR-code")
async def create_qr(message: types.Message):
    global qr_code_text
    qr_code_text = message.text
    await message.reply("Отлично!\nТеперь отправь мне ссылку, для которой нужно создать QR-код.")

@dp.message_handler(lambda message: message.text.startswith('http'))
async def generate_qr_code(message: types.Message):
    global qr_code_text
    url = message.text
    qr_code = qrcode.make(url)
    qr_code.save("metanit_qr.png")
    
    with open("metanit_qr.png", "rb") as qr_image:
        await bot.send_photo(message.chat.id, qr_image, caption=f"Вот твой QR-код для ссылки: {url}", parse_mode=None)
    
    qr_code_text = ""
# qr_code = segno.make_qr("")

#ParseMode.MARKDOWN qr_code.save("metanit_qr.png")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)