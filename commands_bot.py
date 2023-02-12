import random
import time
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters)



def draw(name_one: str, name_two: str) -> list[str]:
    result = random.randint(1, 2)
    if result == 1:
        first_player = name_one
        second_player = name_two
    else:
        first_player = name_two
        second_player = name_one
    return first_player, second_player


SWEETS_NUMBER = 100
MAXIMUM_MOVE = 28

player_sweets = {}


async def sweets_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f'''Игра в конфеты с ботом.
На столе лежит {SWEETS_NUMBER} конфет. Играют два игрока делая ход друг после друга.
Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем {MAXIMUM_MOVE} конфет.
Все конфеты оппонента достаются сделавшему последний ход. Сколько конфет нужно взять первому игроку,
чтобы забрать все конфеты у своего конкурента?
/end - выход из игры
        ''')
    sweets_number = SWEETS_NUMBER
    player_one = update.effective_user.first_name
    player_two = str('Бот')
    await update.message.reply_text('Бросаем жребий!')
    time.sleep(3)
    players_list = draw(player_one, player_two)
    print(players_list)

    if players_list[0] != 'Бот':
        await update.message.reply_text('Вы ходите первым!')
        time.sleep(0.5)
        player_sweets[update.effective_user.id] = sweets_number
        await update.message.reply_text("Сколько конфет забираете?")
    else:
        await update.message.reply_text('Я буду ходить первым!')
        time.sleep(1)
        bots_move = random.randint(1, MAXIMUM_MOVE)
        player_sweets[update.effective_user.id] = sweets_number
        player_sweets[update.effective_user.id] -= bots_move
        await update.message.reply_text(
            f"Убираем со стола {bots_move} конфет\n"
            "\n"
            f"На столе остается {player_sweets[update.effective_user.id]} конфет")
        time.sleep(2)
        await update.message.reply_text("Ваш ход! Сколько конфет забираете?")
    return 1


async def after_move(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        sweets = int(update.message.text)
        if sweets <= player_sweets[update.effective_user.id]:
            if 0 < sweets <= MAXIMUM_MOVE:
                player_sweets[update.effective_user.id] -= sweets
            else:
                await update.message.reply_text(f"Вы хотите забрать конфет больше, чем можно. Попробуйте еще раз!")
                return 1
        else:
            await update.message.reply_text(f"Вы хотите забрать конфет больше, чем есть на столе. Попробуй еще раз!")
            return 1
    except ValueError:
        time.sleep(2)
        await update.message.reply_text(f"Попробуйте еще раз!")
        return 1
    if player_sweets[update.effective_user.id] > 0:
        await update.message.reply_text(f"На столе остается {player_sweets[update.effective_user.id]} конфет")
    else:
        await update.message.reply_text("На столе больше нет конфет(")
        time.sleep(1)
        await update.message.reply_text(f"Вы победили!")
        return ConversationHandler.END
    time.sleep(2)
    bots_move = random.randint(1, MAXIMUM_MOVE)
    await update.message.reply_text(f"Мой ход!")
    if bots_move < player_sweets[update.effective_user.id]:
        player_sweets[update.effective_user.id] -= bots_move
        print(player_sweets[update.effective_user.id])
    else:
        bots_move = player_sweets[update.effective_user.id]
        player_sweets[update.effective_user.id] = 0
    await update.message.reply_text(f"Убираем со стола {bots_move} конфет")
    if player_sweets[update.effective_user.id] > 0:
        await update.message.reply_text(f"На столе остается {player_sweets[update.effective_user.id]} конфет")
        await update.message.reply_text("Ваш ход! Сколько конфет забираете?")
        return 1
    else:
        await update.message.reply_text("На столе больше нет конфет(")
        time.sleep(1)
        await update.message.reply_text(f"Я победил!")
        time.sleep(1)
        del player_sweets[update.effective_user.id]
        return ConversationHandler.END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("До встречи в следующей игре!")
    time.sleep(1)
    del player_sweets[update.effective_user.id]
    return ConversationHandler.END