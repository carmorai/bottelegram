import os
import stripe
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Pagar", url='https://www.carlosmorenoo.com')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Haz clic en el botón para realizar el pago:", reply_markup=reply_markup)

def main():
    token = "6307738962:AAEOr7Xel_u9t_vL1SFDcK-7iTFv26lYHzY"
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()