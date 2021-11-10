from warnings import filters
from telegram.ext import *
from telegram import *
from secret import api_token


players = {}

photo1 = open('1.png', 'rb')
photo2 = open('2.png', 'rb')

JOIN, CHOOSE, SOLVE = range(3)

def start(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в Mat Racing!")
    update.message.reply_text(
        'Игра уже идет! Чтобы принять участие введи свое имя!'
        )

    return JOIN


def join_game(update, context):
    reply_keyboard = [[1, 2]]

    players[update.effective_chat.id] = {'name': update.message.text, 'score': 0}

    update.message.reply_text(
        'Отлично! Вот первые два задания для тебя!'
    )
    update.message.reply_media_group(
        [InputMediaPhoto(open('1.png', 'rb')), InputMediaPhoto(open('2.png', 'rb'))]
    )
    update.message.reply_text(
        'Теперь тебе надо выбрать на какой пример ты будешь отвечать:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='1 или 2?'
        )
    )
    
    return CHOOSE


def choose_problem(update, handler):
    problem_no = update.message.text
    update.message.reply_text(
        f'Ответ к заданию {problem_no}:'
    )
    print(players)

    return SOLVE


def solve_problem(update, handler):
    return SOLVE
    return CHOOSE
    return ConversationHandler.END


def bot() -> None:
    """Run the bot."""
    updater = Updater(api_token)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            JOIN: [MessageHandler(Filters.text & ~Filters.command, join_game)],
            CHOOSE: [MessageHandler(Filters.text & ~Filters.command, choose_problem)],
            SOLVE: [MessageHandler(Filters.text & ~Filters.command, solve_problem)]
        },
        fallbacks=[CommandHandler('quit', quit)],
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    bot()