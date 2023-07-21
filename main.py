import qrcode
from env import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from questions import questions
from qrcode import *
from qrcode import save_qrcode_size
def start_func(update,context):
    update.message.reply_text(text=f"<strong><i>Salom {update.message.from_user.username}! Ushbu bot orqali siz python bo'yicha savollarga javob berishingiz yoki qrcode yasashingiz mumkin.</i></strong>",parse_mode="html")
    my_commands=[
        BotCommand("start",description="Botni ishga tushirish!"),
        BotCommand("savol",description="Savol-javob o'tkazish?"),
        BotCommand("qr_code",description="Qrcode yaratish")
    ]
    context.bot.set_my_commands(my_commands)

def savol_javob(update, context):

    buttons = [
        [InlineKeyboardButton(text=f"{questions[0]['a']}", callback_data="a")],
         [InlineKeyboardButton(text=f"{questions[0]['b']}", callback_data="b")],
        [InlineKeyboardButton(text=f"{questions[0]['c']}", callback_data="c")]
    ]
    context.user_data['question_index'] = 0
    context.user_data['trues'] = 0
    update.message.reply_text(
        text=f"{questions[0]['Savol']}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def message_handler(update, context):
    pass

def inline_messages(update, context):
    query = update.callback_query
    if query.data in ['a','b','c']:
        question_index = context.user_data.get("question_index",0)
        #######################
        if query.data == questions[question_index]["Javob"]:
            context.user_data["trues"] +=1
        ###################

        if question_index < len(questions)-1:
            buttons = [
                [InlineKeyboardButton(text=f"{questions[question_index + 1]['a']}", callback_data="a")],
                [InlineKeyboardButton(text=f"{questions[question_index + 1]['b']}", callback_data="b")],
                [InlineKeyboardButton(text=f"{questions[question_index + 1]['c']}", callback_data="c")]
            ]
            query.message.edit_text(
                text=f"{questions[question_index+1]['Savol']}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            context.user_data['question_index'] = question_index + 1
        else:
#######################################################
            query.message.edit_text(text=f"Test tugadi! To'g'ri javoblaringiz {context.user_data['trues']}/{len(questions)}")
    if context.user_data['trues']==7:
        context.bot.send_animation(chat_id=update.effective_chat.id,animation=open("sigma.mp4","rb"),caption="Ajoyib:)")
#######################################################

updater = Updater(token=TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start',start_func))
dp.add_handler(CommandHandler('savol',savol_javob))
conv_handler = ConversationHandler(
        entry_points=[CommandHandler('qr_code', qrcode_name)],
        states={
            QR_CODE_NAME: [MessageHandler(Filters.text & ~Filters.command, qrcode_result)],
            QR_CODE_RESULT: [MessageHandler(Filters.text & ~Filters.command, qrcode_size)],
            QR_CODE_SIZE: [MessageHandler(Filters.text & ~Filters.command, save_qrcode_size)],
        },
        fallbacks=[],
    )

    # Add the conversation handler to the dispatcher
dp.add_handler(conv_handler)
dp.add_handler(MessageHandler(Filters.document,save_qrcode_size))
dp.add_handler(MessageHandler(Filters.text, message_handler))
dp.add_handler(CallbackQueryHandler(inline_messages))
updater.start_polling()
updater.idle()
