import stripe
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Configurar tu clave secreta de API de Stripe
stripe.api_key = "sk_live_sWrF2uPsg8pBfIiPPPNxPHH4"  # Reemplaza con tu clave secreta de Stripe

def start(update: Update, context: CallbackContext) -> None:
    message = (
        "Suscripción mensual Premium\n\n"
        "Acceso mensual a nuestro grupo privado de Telegram\n\n"
        "TUS BENEFICIOS:\n"
        "✅ NEUROEMPRENDEDOR (Acceso al grupo + 2 grupos adicionales)\n\n"
        "Precio: 8,50€\n"
        "Periodo: 1 mes\n"
        "Modo: Recurrente\n\n"
        "Seleccione una opción:"
    )

    keyboard = [
        [InlineKeyboardButton("Tarjeta de Crédito", url='https://buy.stripe.com/3csaGcaeq92Ggx2001')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

def main():
    # Token de acceso de tu bot
    token = "6307738962:AAEOr7Xel_u9t_vL1SFDcK-7iTFv26lYHzY"  # Reemplaza con tu token real
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Manejador para el comando /start
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()