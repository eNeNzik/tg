import asyncio
from datetime import datetime
import logging
from aiogram.fsm.context import FSMContext
#import config

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    BufferedInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6521406530:AAHa6mkkzD665htwNlz70qln6v2V_GQfDq0")
dp = Dispatcher()
action= ["чорний хліб", "білий хліб", "яблуко", "банан", "апельсин", "паперові серветки", "плюшевий мішка", "менше ніж пів пачки чіпсів", "печиво"]
action2= {action[0]:19.99, action[1]:25, action[2]:59999.99, action[3]:15, action[4]:19.99, action[5]:37, action[6]:999.99, action[7]:64, action[8]:29.99}
def get_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="чорний хліб", callback_data=action[0]),
            InlineKeyboardButton(text="білий хліб", callback_data=action[1]),
            InlineKeyboardButton(text="яблуко", callback_data=action[2]),
        ],
        [
            InlineKeyboardButton(text="банан", callback_data=action[3]),
            InlineKeyboardButton(text="апельсин", callback_data=action[4]),
            InlineKeyboardButton(text="паперові серветки", callback_data=action[5])
        ],
        [
            InlineKeyboardButton(text="плюшевий мішка", callback_data=action[6]),
            InlineKeyboardButton(text="чіпси", callback_data=action[7]),
            InlineKeyboardButton(text="печиво", callback_data=action[8])
        ],
        [   InlineKeyboardButton(text="я не буду купувати по акції", callback_data="None")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
shop2 = []
name_prod = []
def products():
    global shop
    shop = {}
    k = open("products.txt", "r")
    l = k.readlines()
    for i in l:
        shop[i[:i.index(":")]] = i[i.index(":")+1:]
    global shop2
    for i in l:
        name_prod.append(i[:i.index(":")])
    shop2 = []
    for i in l :
        shop2.append([InlineKeyboardButton(text=i+"грн", callback_data=i[:i.index(":")])])
    lp = InlineKeyboardMarkup(inline_keyboard=shop2)
    return lp
@dp.message(Command("shop"))
async def cmd_answer(message: types.Message,state: FSMContext):
    await message.answer(" наявності такі товари:",reply_markup =products())
@dp.callback_query(F.data.in_(name_prod))
async def start(callback: types.CallbackQuery):
    hroshi = 0
    await callback.message.answer(f"Ви купили {callback.data} за {shop[callback.data]} грн")
    hrn = open("гаманець.txt", "r")
    save_data = hrn.readlines()
    new_user = True
    for money in save_data:
        if callback.message.from_user.full_name in money:
            hroshi = money[money.index(":") + 1:]
            await callback.message.answer(f"на вашому рахунку {round(float(hroshi) - int(shop[callback.data]), 2)} грн")
            new_user = False
            break
    hrn.close()
def update_file(message):
    print("1")
    with open("information.txt", "a") as file:
        print("2")
        file.write(f"User wrote {message.text} to your bot\n")
        file.write(f"Full name this user: {message.from_user.full_name}\n")
        file.write(f"ID this user: {message.from_user.id}\n")
        file.write(f"Time when this user spoke with youre telegram: {datetime.now()}\n\n")
        print("3")
@dp.message(Command("start"))
async def cmd_answer(message: types.Message):
    update_file(message)
    await message.answer(f"Привіт, {message.from_user.full_name}, Вас вітає магазин 'Сільпо'")
    await message.answer("Пропонуємо знижку на такі товари:",reply_markup = get_keyboard())
# @dp.callback_query(F.data.in_(action))
# async def cmd_answer(callback: types.CallbackQuery):
#     await callback.message.answer(callback.data)
@dp.callback_query(F.data.in_(action))
async def start(callback: types.CallbackQuery):
    hroshi = 0
    await callback.message.answer(f"Ви купили {callback.data} за {action2[callback.data]} грн")
    hrn = open("гаманець.txt", "r")
    save_data = hrn.readlines()
    new_user = True
    for money in save_data:
        if callback.message.from_user.full_name in money:
            hroshi = money[money.index(":") + 1:]
            await callback.message.answer(f"на вашому рахунку {round(float(hroshi) - action2[callback.data], 2)} грн")
            new_user = False
            break
    hrn.close()
    if new_user == True:
        hrn = open("гаманець.txt", "a")
        hrn.write(callback.message.from_user.full_name + ":" + "5000" + "\n")
        hrn.close()
    else:
        hrn = open("гаманець.txt", "w")
        for d in save_data:
            if callback.message.from_user.full_name in d:
                save_data[save_data.index(d)] = callback.message.from_user.full_name + ":" + str(float(hroshi) - action2[callback.data])
                break
        hrn.writelines(save_data)
        hrn.close()
add = ""
price = ""

class Status(StatesGroup):
    status1 = State()
    sasha = State()
@dp.message(Command("add"))
async def cmd_answer(message: types.Message,state: FSMContext):
    await message.answer("що ви хочете додати?")
    await state.set_state(Status.status1)
@dp.message(F.text, Status.status1)
async def cmd_answer(message: types.Message,state: FSMContext):
    global add
    add = message.text
    await state.set_state(Status.sasha)
    await message.answer("яка ціна "+add)
@dp.message(Command("shop"))
async def cmd_answer(message: types.Message,state: FSMContext):
    await message.answer()

@dp.message(F.text, Status.sasha)
async def cmd_answer(message: types.Message, state: FSMContext):
    price = message.text
    l = open("products.txt", "a")
    l.write(add+":"+price+"\n")
    l.close()
    await state.clear()

@dp.callback_query(F.data == "None")
async def start(callback: types.CallbackQuery):
    await callback.message.delete()

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())