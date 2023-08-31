import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

def start(update: Update, context: CallbackContext) -> None:
    message = (
        "Suscripción mensual Premium\n\n"
        "Acceso mensual a nuestro grupo privado de Telegram\n\n"
        "TUS BENEFICIOS:\n"
        "✅ NEUROEMPRENDEDOR (Acceso al grupo + 2 grupos adicionales)\n\n"
        "Price: 8,50 €\n"
        "Periodo: 1 month\n"
        "Modo: Recurrente\n\n"
        "Seleccione una opción:"
    )

    keyboard = [
        [InlineKeyboardButton("Tarjeta ELOI de Crédito", callback_data='stripe')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # Acknowledge the button click

    if query.data == 'stripe':
        # Aquí puedes implementar la lógica para manejar los pagos con Stripe
        message = "Haz clic en el enlace para realizar el pago con tarjeta de crédito."
        query.message.reply_text(message)

def main():
    # Token de acceso de tu bot
    token = "6307738962:AAEOr7Xel_u9t_vL1SFDcK-7iTFv26lYHzY"  # Reemplaza con tu token real
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Manejador para el comando /start
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Manejador para los botones
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    
    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
