import asyncio
import logging
import random
import sys
import time

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
import json

TOKEN = "" # Token from Bot Father
auth_waiting = []
users = []
admins = []
ban = []
nicknames = {}
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
creator = 000000000 # Your Creator id

async def send_to_admins(smt: str):
    for admin in admins:
        await bot.send_message(admin, smt)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    nicknames[str(message.chat.id)] = str(message.chat.username)
    update_json()
    if message.chat.id in ban:
        pass

    elif message.chat.id not in admins and message.chat.id not in users:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)} !\nAuthorization in progress.")
        auth_waiting.append(message.chat.id)
        await send_to_admins(
            f"New user requesting authorization \nId: {message.chat.id} \nName: {message.chat.username}")

    elif message.chat.id not in admins and message.chat.id in users:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}! You are authorized, wait for test.")

    elif message.chat.id in admins:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)} !\n"
                             f"You are an admin.\n "
                             f"Bot is running\n")
        if auth_waiting:
            await message.answer(f"Waiting for authorization:\n")
            for i in auth_waiting:
                await message.answer(str(i))


@dp.message()
async def echo_handler(message: types.Message) -> None:
    nicknames[str(message.chat.id)] = str(message.chat.username)
    update_json()
    if message.chat.id in ban:
        pass

    elif message.chat.id not in admins:
        await message.answer("Only admins can chat with the bot.\n"
                             "If you want to tell something to admins or to add the teacher write to: @\n" # tg username admin
                             "If you want respect from historic person use /respect.")

    else:
        text = message.text.split()
        if text[0] == '/allow':

            if int(text[1]) in auth_waiting:
                users.append(int(text[1]))
                auth_waiting.remove(int(text[1]))
                await bot.send_message(int(text[1]), str("You are authorized! \nEnjoy!"))
                await send_to_admins(f"New user authorized {text[1]} by {message.chat.id}")
                update_json()

            else:
                await message.answer("No such user, waiting for authorization.")

        elif text[0] == '/deny':
            if int(text[1]) in auth_waiting:
                auth_waiting.remove(int(text[1]))
                await bot.send_message(int(text[1]), str("Permission denied."))
                await bot.send_message(message.chat.id, f"Authorisation of user {text[1]} denied")
                await bot.send_message(creator, f"User {message.chat.id} denied {int(text[1])}.")

                update_json()
            else:
                await message.answer("No such user, waiting for authorization.")

        elif text[0] == '/help':
            await bot.send_message(message.chat.id, "God bless you!")

        elif text[0] == '/admin':
            if message.chat.id == creator:
                if int(text[1]) in admins:
                    await bot.send_message(message.chat.id, "Users is already an admin.")
                elif int(text[1]) not in users:
                    await bot.send_message(message.chat.id, "Wrong user.")

                elif int(text[1]) in ban:
                    await bot.send_message(message.chat.id, 'User in ban')

                elif int(text[1]) in users:
                    admins.append(int(text[1]))
                    await send_to_admins(f"User {int(text[1])} upgraded to admin by {message.chat.id}")
                    await bot.send_message(int(text[1]), "Now you`re an admin. Enjoy...")

            else:
                await bot.send_message(message.chat.id, "Only the creator can make admins.")
                await bot.send_message(creator, f"User {message.chat.id} tried to make admin user {int(text[1])}.")

        elif text[0] == '/text':
            await tell_user(' '.join(text[1:]))
            if message.chat.id != creator:
                await bot.send_message(creator, f"User {message.chat.id} text to all {' '.join(text[1:])}.")


        elif text[0] == '/textto':
            try:
                if int(text[1]) not in users:
                    await bot.send_message(message.chat.id, "No such user.")
                else:
                    await bot.send_message(int(text[1]), ' '.join(text[2:]))
                    if int(text[1]) != creator:
                        await bot.send_message(creator,
                                               f"User {message.chat.id} texted to {text[1]} this {' '.join(text[2:])}.")

            except Exception:
                await bot.send_message(message.chat.id, f"No such command, use /help")
        elif text[0] == '/users':
            await bot.send_message(message.chat.id, str(users))

        elif text[0] == '/all':
            await bot.send_message(message.chat.id, str(nicknames))

        elif text[0] == '/banned':
            await bot.send_message(message.chat.id, str(ban))

        elif text[0] == '/save':
            await bot.send_document(message.chat.id, FSInputFile(path='data.json'))
            await bot.send_document(message.chat.id, FSInputFile(path='users.json'))
            if message.chat.id != creator:
                await bot.send_message(creator, f"User {message.chat.id} save files.")

        elif text[0] == '/ban':
            if int(text[1]) == creator:
                await bot.send_message(message.chat.id, "You can`t ban the creator.")
                await bot.send_message(creator, f"User {message.chat.id} tried to ban you.")
            else:
                ban.append(int(text[1]))
                try:
                    users.remove(int(text[1]))
                    admins.remove(int(text[1]))
                except ValueError:
                    pass
                finally:
                    await send_to_admins(f"User {text[1]} was banned by {message.chat.id}")
                    update_json()

        elif text[0] == '/free':
            ban.remove(int(text[1]))
            await bot.send_message(message.chat.id, f"User {text[1]} is free. ")
            await send_to_admins(f"User {text[1]} released from ban by {message.chat.id}")
            update_json()

        elif text[0] == '/delete':
            if int(text[1]) == creator:
                await bot.send_message(message.chat.id, "You can`t delete the creator.")
                await bot.send_message(creator, f"User {message.chat.id} tried to delete you.")
            else:
                await bot.send_message(int(text[1]), 'Administrator deleted you.')
                users.remove(int(text[1]))
                await send_to_admins(f"User {text[1]} was successfully deleted by {message.chat.id}")
                update_json()

        else:
            await bot.send_message(message.chat.id, f"No such command, use /help")


def update_json():
    try:
        with open('users.json', 'w') as f:
            data = {}
            data['admins'] = admins
            data['users'] = users
            data['ban'] = ban
            data['nicknames'] = nicknames
            json.dump(data, f)
            del data
    except Exception as e:
        exit(e)


async def tell_user(text: str):
    for i in users:
        await bot.send_message(i, text)


async def main() -> None:
    await dp.start_polling(bot)


async def broadcaster(st: str):
    try:
        await tell_user(st)
    except Exception as e:
        exit(e)


async def get_info():
    print("begin")
    while True:
        r = random.randrange(0, 10)
        time.sleep(r)
        await broadcaster(str(r * 19))


if __name__ == "__main__":
    try:
        with open('users.json', 'r', errors='ignore') as file:
            data = dict(json.load(file))
            print(data)
            users = data.get('users')
            admins = data.get('admins')
            nicknames = dict(data.get('nicknames'))
            ban = data.get('ban')

    except FileNotFoundError:
        exit("Add users.json file")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # asyncio.run(get_info()) # Do smt and send it to users
    asyncio.run(main())
