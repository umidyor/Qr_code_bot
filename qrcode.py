import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

# States
QR_CODE_NAME, QR_CODE_RESULT, QR_CODE_SIZE, END = range(4)

def validate_qr_code_name(text):
    # Using regular expression to validate the qrcode_name input
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', text))

def validate_qr_code_result(text):
    # Using regular expression to validate the qrcode_result input
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', text))

def validate_qr_code_size(text):
    # Using regular expression to validate the qrcode_size input (1-5)
    return bool(re.match(r'^[1-5]$', text))

def qrcode_name(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Qrcode uchun nom yozing...")
    return QR_CODE_NAME

def qrcode_result(update: Update, context: CallbackContext) -> int:

    context.user_data["qrcode_name"] = update.message.text
    update.message.reply_text("Qrcode dan chiqadigan natijani yozing...")
    return QR_CODE_RESULT

def qrcode_size(update: Update, context: CallbackContext) -> int:

    context.user_data["qrcode_result"] = update.message.text
    update.message.reply_text("Qrcodening razmerini yozing (1-5)..")
    return QR_CODE_SIZE


def save_qrcode_size(update: Update, context: CallbackContext) -> int:
    if validate_qr_code_size(update.message.text):
        context.user_data["qrcode_size"] = update.message.text

        # Now you have all the information collected from the conversation.
        # You can access and use it as needed.
        qrcode_name = context.user_data.get("qrcode_name")
        qrcode_result = context.user_data.get("qrcode_result")
        qrcode_size = context.user_data.get("qrcode_size")

        # Do something with the collected information...
        # For example, print it:
        update.message.reply_text(f"Qrcode Name: {qrcode_name}\nQrcode Result: {qrcode_result}\nQrcode Size: {qrcode_size}")
        import pyqrcode

        qrcode = pyqrcode.create(qrcode_result, error='L', version=10)
        qrcode.png(f"images/{qrcode_name}.png", scale=qrcode_size)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f"images/{qrcode_name}.png","rb"),caption="Marhamat!Tayyor😉")

        # End the conversation
        return END
    else:
        update.message.reply_text("Bu o'lcham juda ham katta😒")
        return QR_CODE_SIZE




